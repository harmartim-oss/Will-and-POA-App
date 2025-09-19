import jwt
import secrets
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, current_app
from src.models.user import User, UserSession, UserActivity, db
import re

class AuthService:
    def __init__(self, app=None):
        self.app = app
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize the auth service with Flask app."""
        app.config.setdefault('JWT_SECRET_KEY', secrets.token_urlsafe(32))
        app.config.setdefault('JWT_EXPIRATION_HOURS', 24)
        app.config.setdefault('SESSION_EXPIRATION_HOURS', 168)  # 7 days
    
    def register_user(self, username, email, password, **kwargs):
        """Register a new user."""
        try:
            # Validate input
            validation_result = self._validate_registration_data(username, email, password)
            if not validation_result['valid']:
                return {
                    'success': False,
                    'errors': validation_result['errors']
                }
            
            # Check if user already exists
            if User.query.filter_by(username=username).first():
                return {
                    'success': False,
                    'errors': ['Username already exists']
                }
            
            if User.query.filter_by(email=email).first():
                return {
                    'success': False,
                    'errors': ['Email already registered']
                }
            
            # Create new user
            user = User(
                username=username,
                email=email,
                first_name=kwargs.get('first_name'),
                last_name=kwargs.get('last_name'),
                phone_number=kwargs.get('phone_number'),
                address=kwargs.get('address')
            )
            user.set_password(password)
            user.generate_verification_token()
            
            db.session.add(user)
            db.session.commit()
            
            # Log registration activity
            self._log_user_activity(user.id, 'registration', 'User registered successfully')
            
            return {
                'success': True,
                'user': user.to_dict(),
                'verification_token': user.email_verification_token
            }
            
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'errors': [f'Registration failed: {str(e)}']
            }
    
    def authenticate_user(self, username_or_email, password, ip_address=None, user_agent=None):
        """Authenticate user and create session."""
        try:
            # Find user by username or email
            user = User.query.filter(
                (User.username == username_or_email) | (User.email == username_or_email)
            ).first()
            
            if not user:
                return {
                    'success': False,
                    'errors': ['Invalid credentials']
                }
            
            # Check if account is locked
            if user.is_account_locked():
                return {
                    'success': False,
                    'errors': ['Account is temporarily locked due to multiple failed login attempts']
                }
            
            # Check password
            if not user.check_password(password):
                user.increment_login_attempts()
                db.session.commit()
                
                self._log_user_activity(user.id, 'failed_login', 'Failed login attempt', {
                    'ip_address': ip_address,
                    'user_agent': user_agent
                })
                
                return {
                    'success': False,
                    'errors': ['Invalid credentials']
                }
            
            # Check if account is active
            if not user.is_active:
                return {
                    'success': False,
                    'errors': ['Account is deactivated']
                }
            
            # Successful login
            user.reset_login_attempts()
            
            # Create session
            session = self._create_user_session(user, ip_address, user_agent)
            
            # Generate JWT token
            jwt_token = self._generate_jwt_token(user)
            
            db.session.commit()
            
            # Log successful login
            self._log_user_activity(user.id, 'login', 'User logged in successfully', {
                'ip_address': ip_address,
                'user_agent': user_agent,
                'session_id': session.id
            })
            
            return {
                'success': True,
                'user': user.to_dict(),
                'token': jwt_token,
                'session': session.to_dict()
            }
            
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'errors': [f'Authentication failed: {str(e)}']
            }
    
    def verify_token(self, token):
        """Verify JWT token and return user."""
        try:
            payload = jwt.decode(
                token,
                current_app.config['JWT_SECRET_KEY'],
                algorithms=['HS256']
            )
            
            user_id = payload.get('user_id')
            if not user_id:
                return None
            
            user = User.query.get(user_id)
            if not user or not user.is_active:
                return None
            
            return user
            
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def verify_session(self, session_token):
        """Verify session token and return user."""
        try:
            session = UserSession.query.filter_by(
                session_token=session_token,
                is_active=True
            ).first()
            
            if not session or session.is_expired():
                if session:
                    session.is_active = False
                    db.session.commit()
                return None
            
            # Update last activity
            session.last_activity = datetime.utcnow()
            db.session.commit()
            
            return session.user
            
        except Exception:
            return None
    
    def logout_user(self, session_token=None, user_id=None):
        """Logout user by invalidating session."""
        try:
            if session_token:
                session = UserSession.query.filter_by(session_token=session_token).first()
                if session:
                    session.is_active = False
                    self._log_user_activity(session.user_id, 'logout', 'User logged out')
            
            elif user_id:
                # Logout all sessions for user
                sessions = UserSession.query.filter_by(user_id=user_id, is_active=True).all()
                for session in sessions:
                    session.is_active = False
                self._log_user_activity(user_id, 'logout_all', 'All sessions logged out')
            
            db.session.commit()
            return {'success': True}
            
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    def change_password(self, user_id, current_password, new_password):
        """Change user password."""
        try:
            user = User.query.get(user_id)
            if not user:
                return {'success': False, 'errors': ['User not found']}
            
            # Verify current password
            if not user.check_password(current_password):
                return {'success': False, 'errors': ['Current password is incorrect']}
            
            # Validate new password
            validation_result = self._validate_password(new_password)
            if not validation_result['valid']:
                return {'success': False, 'errors': validation_result['errors']}
            
            # Set new password
            user.set_password(new_password)
            db.session.commit()
            
            # Log password change
            self._log_user_activity(user_id, 'password_change', 'Password changed successfully')
            
            return {'success': True}
            
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'errors': [str(e)]}
    
    def request_password_reset(self, email):
        """Request password reset token."""
        try:
            user = User.query.filter_by(email=email).first()
            if not user:
                # Don't reveal if email exists
                return {'success': True, 'message': 'If email exists, reset instructions have been sent'}
            
            # Generate reset token
            reset_token = user.generate_password_reset_token()
            db.session.commit()
            
            # Log password reset request
            self._log_user_activity(user.id, 'password_reset_request', 'Password reset requested')
            
            return {
                'success': True,
                'reset_token': reset_token,
                'message': 'Password reset instructions have been sent'
            }
            
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'errors': [str(e)]}
    
    def reset_password(self, reset_token, new_password):
        """Reset password using reset token."""
        try:
            user = User.query.filter_by(password_reset_token=reset_token).first()
            
            if not user or not user.password_reset_expires or user.password_reset_expires < datetime.utcnow():
                return {'success': False, 'errors': ['Invalid or expired reset token']}
            
            # Validate new password
            validation_result = self._validate_password(new_password)
            if not validation_result['valid']:
                return {'success': False, 'errors': validation_result['errors']}
            
            # Set new password and clear reset token
            user.set_password(new_password)
            user.password_reset_token = None
            user.password_reset_expires = None
            
            db.session.commit()
            
            # Log password reset
            self._log_user_activity(user.id, 'password_reset', 'Password reset successfully')
            
            return {'success': True}
            
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'errors': [str(e)]}
    
    def verify_email(self, verification_token):
        """Verify user email using verification token."""
        try:
            user = User.query.filter_by(email_verification_token=verification_token).first()
            
            if not user:
                return {'success': False, 'errors': ['Invalid verification token']}
            
            user.is_verified = True
            user.email_verification_token = None
            db.session.commit()
            
            # Log email verification
            self._log_user_activity(user.id, 'email_verified', 'Email verified successfully')
            
            return {'success': True, 'user': user.to_dict()}
            
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'errors': [str(e)]}
    
    def require_auth(self, f):
        """Decorator to require authentication."""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = None
            
            # Check for JWT token in Authorization header
            auth_header = request.headers.get('Authorization')
            if auth_header and auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
            
            # Check for session token in cookies
            session_token = request.cookies.get('session_token')
            
            user = None
            
            if token:
                user = self.verify_token(token)
            elif session_token:
                user = self.verify_session(session_token)
            
            if not user:
                return jsonify({'error': 'Authentication required'}), 401
            
            # Add user to request context
            request.current_user = user
            
            return f(*args, **kwargs)
        
        return decorated_function
    
    def require_verified_email(self, f):
        """Decorator to require verified email."""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not hasattr(request, 'current_user') or not request.current_user.is_verified:
                return jsonify({'error': 'Email verification required'}), 403
            
            return f(*args, **kwargs)
        
        return decorated_function
    
    def require_subscription(self, required_level='premium'):
        """Decorator to require specific subscription level."""
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                if not hasattr(request, 'current_user'):
                    return jsonify({'error': 'Authentication required'}), 401
                
                user_level = request.current_user.subscription_type
                
                # Define subscription hierarchy
                levels = {'free': 0, 'premium': 1, 'professional': 2}
                
                if levels.get(user_level, 0) < levels.get(required_level, 1):
                    return jsonify({'error': f'{required_level.title()} subscription required'}), 403
                
                return f(*args, **kwargs)
            
            return decorated_function
        return decorator
    
    # Private helper methods
    
    def _validate_registration_data(self, username, email, password):
        """Validate registration data."""
        errors = []
        
        # Username validation
        if not username or len(username) < 3:
            errors.append('Username must be at least 3 characters long')
        elif not re.match(r'^[a-zA-Z0-9_]+$', username):
            errors.append('Username can only contain letters, numbers, and underscores')
        
        # Email validation
        if not email or not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            errors.append('Valid email address is required')
        
        # Password validation
        password_validation = self._validate_password(password)
        if not password_validation['valid']:
            errors.extend(password_validation['errors'])
        
        return {'valid': len(errors) == 0, 'errors': errors}
    
    def _validate_password(self, password):
        """Validate password strength."""
        errors = []
        
        if not password or len(password) < 8:
            errors.append('Password must be at least 8 characters long')
        
        if not re.search(r'[A-Z]', password):
            errors.append('Password must contain at least one uppercase letter')
        
        if not re.search(r'[a-z]', password):
            errors.append('Password must contain at least one lowercase letter')
        
        if not re.search(r'\d', password):
            errors.append('Password must contain at least one number')
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.append('Password must contain at least one special character')
        
        return {'valid': len(errors) == 0, 'errors': errors}
    
    def _create_user_session(self, user, ip_address=None, user_agent=None):
        """Create a new user session."""
        session_token = secrets.token_urlsafe(32)
        expires_at = datetime.utcnow() + timedelta(hours=current_app.config['SESSION_EXPIRATION_HOURS'])
        
        session = UserSession(
            user_id=user.id,
            session_token=session_token,
            ip_address=ip_address,
            user_agent=user_agent,
            expires_at=expires_at
        )
        
        db.session.add(session)
        return session
    
    def _generate_jwt_token(self, user):
        """Generate JWT token for user."""
        payload = {
            'user_id': user.id,
            'username': user.username,
            'exp': datetime.utcnow() + timedelta(hours=current_app.config['JWT_EXPIRATION_HOURS']),
            'iat': datetime.utcnow()
        }
        
        return jwt.encode(
            payload,
            current_app.config['JWT_SECRET_KEY'],
            algorithm='HS256'
        )
    
    def _log_user_activity(self, user_id, activity_type, description, metadata=None):
        """Log user activity."""
        try:
            activity = UserActivity(
                user_id=user_id,
                activity_type=activity_type,
                description=description,
                metadata=metadata,
                ip_address=request.remote_addr if request else None
            )
            
            db.session.add(activity)
            
        except Exception:
            # Don't fail the main operation if logging fails
            pass

# Global auth service instance
auth_service = AuthService()

