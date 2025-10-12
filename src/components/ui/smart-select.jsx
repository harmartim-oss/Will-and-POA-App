import React, { useState } from 'react';
import { Label } from './label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './select';
import { Input } from './input';
import { Textarea } from './textarea';
import { Button } from './button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './card';
import { Badge } from './badge';
import { HelpCircle, Lightbulb, Info, X } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from './tooltip';

/**
 * SmartSelect - An intelligent select component with help text and "Other" option
 * Includes AI-powered tips and explanatory guidance
 */
export const SmartSelect = ({ 
  label, 
  value, 
  onChange, 
  options, 
  placeholder = "Select an option",
  helpText = null,
  showAITips = false,
  aiTips = [],
  required = false,
  description = null,
  className = ""
}) => {
  const [showHelp, setShowHelp] = useState(false);
  const [showOtherInput, setShowOtherInput] = useState(false);
  const [otherValue, setOtherValue] = useState('');

  const handleValueChange = (newValue) => {
    if (newValue === 'other') {
      setShowOtherInput(true);
      onChange(''); // Clear the value until user enters custom text
    } else {
      setShowOtherInput(false);
      onChange(newValue);
    }
  };

  const handleOtherSubmit = () => {
    if (otherValue.trim()) {
      onChange(otherValue);
      setShowOtherInput(false);
    }
  };

  return (
    <div className={`space-y-2 ${className}`}>
      <div className="flex items-center justify-between">
        <Label className="flex items-center space-x-2">
          <span>{label}</span>
          {required && <span className="text-red-500">*</span>}
        </Label>
        {helpText && (
          <TooltipProvider>
            <Tooltip>
              <TooltipTrigger asChild>
                <Button
                  variant="ghost"
                  size="sm"
                  className="h-8 w-8 p-0"
                  onClick={() => setShowHelp(!showHelp)}
                  type="button"
                >
                  <HelpCircle className="h-4 w-4 text-blue-600" />
                </Button>
              </TooltipTrigger>
              <TooltipContent>
                <p>Click for detailed help</p>
              </TooltipContent>
            </Tooltip>
          </TooltipProvider>
        )}
      </div>

      {description && (
        <p className="text-sm text-gray-500">{description}</p>
      )}

      <Select value={value} onValueChange={handleValueChange}>
        <SelectTrigger className="w-full">
          <SelectValue placeholder={placeholder} />
        </SelectTrigger>
        <SelectContent>
          {options.map((option) => (
            <SelectItem key={option.value} value={option.value}>
              <div className="flex flex-col">
                <span>{option.label}</span>
                {option.description && (
                  <span className="text-xs text-gray-500">{option.description}</span>
                )}
              </div>
            </SelectItem>
          ))}
        </SelectContent>
      </Select>

      <AnimatePresence>
        {showOtherInput && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="space-y-2"
          >
            <Input
              placeholder="Please specify..."
              value={otherValue}
              onChange={(e) => setOtherValue(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleOtherSubmit()}
            />
            <div className="flex space-x-2">
              <Button size="sm" onClick={handleOtherSubmit}>
                Confirm
              </Button>
              <Button 
                size="sm" 
                variant="outline" 
                onClick={() => {
                  setShowOtherInput(false);
                  setOtherValue('');
                }}
              >
                Cancel
              </Button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      <AnimatePresence>
        {showHelp && helpText && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: 0.2 }}
          >
            <Card className="border-blue-200 bg-blue-50">
              <CardHeader className="pb-3">
                <div className="flex items-start justify-between">
                  <div className="flex items-center space-x-2">
                    <Info className="h-5 w-5 text-blue-600" />
                    <CardTitle className="text-base">{helpText.title}</CardTitle>
                  </div>
                  <Button
                    variant="ghost"
                    size="sm"
                    className="h-6 w-6 p-0"
                    onClick={() => setShowHelp(false)}
                  >
                    <X className="h-4 w-4" />
                  </Button>
                </div>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-sm text-gray-700 mb-3">
                  {helpText.content}
                </CardDescription>
                {helpText.tips && helpText.tips.length > 0 && (
                  <div className="space-y-2">
                    <div className="flex items-center space-x-2 text-sm font-medium text-gray-700">
                      <Lightbulb className="h-4 w-4 text-yellow-600" />
                      <span>Tips:</span>
                    </div>
                    <ul className="space-y-1 ml-6">
                      {helpText.tips.map((tip, index) => (
                        <li key={index} className="text-sm text-gray-600 list-disc">
                          {tip}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </CardContent>
            </Card>
          </motion.div>
        )}
      </AnimatePresence>

      <AnimatePresence>
        {showAITips && aiTips.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
          >
            <Card className="border-purple-200 bg-purple-50">
              <CardHeader className="pb-2">
                <CardTitle className="text-sm flex items-center space-x-2">
                  <Lightbulb className="h-4 w-4 text-purple-600" />
                  <span>AI Suggestions</span>
                  <Badge variant="secondary" className="text-xs">Powered by AI</Badge>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2">
                  {aiTips.map((tip, index) => (
                    <li key={index} className="text-sm text-gray-700">
                      {tip}
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

/**
 * SmartTextarea - Enhanced textarea with character count and help
 */
export const SmartTextarea = ({
  label,
  value,
  onChange,
  placeholder = "",
  helpText = null,
  maxLength = 1000,
  rows = 4,
  required = false,
  description = null,
  suggestions = [],
  className = ""
}) => {
  const [showHelp, setShowHelp] = useState(false);

  return (
    <div className={`space-y-2 ${className}`}>
      <div className="flex items-center justify-between">
        <Label className="flex items-center space-x-2">
          <span>{label}</span>
          {required && <span className="text-red-500">*</span>}
        </Label>
        <div className="flex items-center space-x-2">
          {helpText && (
            <Button
              variant="ghost"
              size="sm"
              className="h-8 w-8 p-0"
              onClick={() => setShowHelp(!showHelp)}
              type="button"
            >
              <HelpCircle className="h-4 w-4 text-blue-600" />
            </Button>
          )}
          {maxLength && (
            <span className="text-xs text-gray-500">
              {value.length}/{maxLength}
            </span>
          )}
        </div>
      </div>

      {description && (
        <p className="text-sm text-gray-500">{description}</p>
      )}

      <Textarea
        value={value}
        onChange={(e) => {
          if (!maxLength || e.target.value.length <= maxLength) {
            onChange(e.target.value);
          }
        }}
        placeholder={placeholder}
        rows={rows}
        className="w-full"
      />

      {suggestions.length > 0 && (
        <div className="space-y-2">
          <p className="text-sm font-medium text-gray-700">Suggestions:</p>
          <div className="flex flex-wrap gap-2">
            {suggestions.map((suggestion, index) => (
              <Button
                key={index}
                variant="outline"
                size="sm"
                onClick={() => onChange(suggestion.template || suggestion)}
                type="button"
                className="text-xs"
              >
                {suggestion.label || suggestion}
              </Button>
            ))}
          </div>
        </div>
      )}

      <AnimatePresence>
        {showHelp && helpText && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
          >
            <Card className="border-blue-200 bg-blue-50">
              <CardHeader className="pb-3">
                <div className="flex items-start justify-between">
                  <div className="flex items-center space-x-2">
                    <Info className="h-5 w-5 text-blue-600" />
                    <CardTitle className="text-base">{helpText.title}</CardTitle>
                  </div>
                  <Button
                    variant="ghost"
                    size="sm"
                    className="h-6 w-6 p-0"
                    onClick={() => setShowHelp(false)}
                  >
                    <X className="h-4 w-4" />
                  </Button>
                </div>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-sm text-gray-700">
                  {helpText.content}
                </CardDescription>
                {helpText.tips && (
                  <ul className="mt-3 space-y-1 ml-4">
                    {helpText.tips.map((tip, index) => (
                      <li key={index} className="text-sm text-gray-600 list-disc">
                        {tip}
                      </li>
                    ))}
                  </ul>
                )}
              </CardContent>
            </Card>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default SmartSelect;
