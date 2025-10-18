import { useEffect, useState } from 'react';
import { useRegisterSW } from 'virtual:pwa-register/react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { RefreshCw, X } from 'lucide-react';

/**
 * PWA Update Prompt Component
 * Shows a notification when a new version of the app is available
 * Allows users to update immediately or dismiss
 */
export function PWAUpdatePrompt() {
  const [showPrompt, setShowPrompt] = useState(false);
  
  const {
    offlineReady: [offlineReady, setOfflineReady],
    needRefresh: [needRefresh, setNeedRefresh],
    updateServiceWorker,
  } = useRegisterSW({
    onRegistered(r) {
      console.log('✅ Service Worker registered:', r);
    },
    onRegisterError(error) {
      console.error('❌ Service Worker registration error:', error);
    },
  });

  useEffect(() => {
    if (offlineReady || needRefresh) {
      setShowPrompt(true);
    }
  }, [offlineReady, needRefresh]);

  const close = () => {
    setShowPrompt(false);
    setOfflineReady(false);
    setNeedRefresh(false);
  };

  const handleUpdate = async () => {
    await updateServiceWorker(true);
  };

  if (!showPrompt) return null;

  return (
    <div className="fixed bottom-4 right-4 z-50 max-w-md">
      <Card className="shadow-lg border-2">
        <CardHeader className="pb-3">
          <div className="flex items-start justify-between">
            <div className="flex items-center gap-2">
              <RefreshCw className="h-5 w-5 text-blue-600" />
              <CardTitle className="text-base">
                {needRefresh ? 'Update Available' : 'App Ready for Offline Use'}
              </CardTitle>
            </div>
            <Button
              variant="ghost"
              size="icon"
              className="h-6 w-6 -mt-1 -mr-2"
              onClick={close}
            >
              <X className="h-4 w-4" />
            </Button>
          </div>
        </CardHeader>
        <CardContent className="pb-3">
          <CardDescription>
            {needRefresh
              ? 'A new version of the Ontario Wills app is available. Reload to get the latest features and improvements.'
              : 'The Ontario Wills app is now available offline. You can use it without an internet connection.'}
          </CardDescription>
        </CardContent>
        <CardFooter className="gap-2">
          {needRefresh && (
            <Button onClick={handleUpdate} className="flex-1">
              <RefreshCw className="mr-2 h-4 w-4" />
              Update Now
            </Button>
          )}
          <Button variant="outline" onClick={close} className={needRefresh ? 'flex-1' : 'w-full'}>
            {needRefresh ? 'Later' : 'Got it'}
          </Button>
        </CardFooter>
      </Card>
    </div>
  );
}

export default PWAUpdatePrompt;
