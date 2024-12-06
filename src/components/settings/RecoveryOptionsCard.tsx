// src/components/settings/RecoveryOptionsCard.tsx
import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { 
  LifeBuoy,
  Mail,
  Phone,
  Plus,
  Trash2,
  CheckCircle2,
  AlertTriangle,
  RefreshCw,
  BadgeCheck,
  Shield
} from 'lucide-react';
import { useToast } from '@/hooks/use-toast';
import { cn } from '@/lib/utils';

interface RecoveryOption {
  id: string;
  type: 'email' | 'phone';
  value: string;
  verified: boolean;
  primary: boolean;
}

interface NewOption {
  type: 'email' | 'phone';
  value: string;
}

export default function RecoveryOptionsCard() {
  const { toast } = useToast();
  const [isAddingNew, setIsAddingNew] = React.useState(false);
  const [isLoading, setIsLoading] = React.useState(false);
  const [newOption, setNewOption] = React.useState<NewOption>({
    type: 'email',
    value: ''
  });

  const [recoveryOptions, setRecoveryOptions] = React.useState<RecoveryOption[]>([
    {
      id: '1',
      type: 'email',
      value: 'primary@example.com',
      verified: true,
      primary: true
    },
    {
      id: '2',
      type: 'phone',
      value: '+91 98765 43210',
      verified: true,
      primary: false
    },
    {
      id: '3',
      type: 'email',
      value: 'backup@example.com',
      verified: false,
      primary: false
    }
  ]);

  const handleTypeChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setNewOption(prev => ({
      ...prev,
      type: e.target.value as 'email' | 'phone'
    }));
  };

  const handleValueChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setNewOption(prev => ({
      ...prev,
      value: e.target.value
    }));
  };

  const validateNewOption = () => {
    if (!newOption.value.trim()) {
      toast({
        title: "Error",
        description: `Please enter a valid ${newOption.type}`,
        variant: "destructive"
      });
      return false;
    }

    if (newOption.type === 'email' && 
        !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(newOption.value)) {
      toast({
        title: "Error",
        description: "Please enter a valid email address",
        variant: "destructive"
      });
      return false;
    }

    if (newOption.type === 'phone' && 
        !/^\+?[\d\s-]{10,}$/.test(newOption.value)) {
      toast({
        title: "Error",
        description: "Please enter a valid phone number",
        variant: "destructive"
      });
      return false;
    }

    return true;
  };

  const handleAddOption = async () => {
    if (!validateNewOption()) return;

    setIsLoading(true);
    try {
      // Here you would make an API call to add the recovery option
      await new Promise(resolve => setTimeout(resolve, 1000));

      const newId = Math.random().toString(36).substring(7);
      setRecoveryOptions(prev => [
        ...prev,
        {
          id: newId,
          ...newOption,
          verified: false,
          primary: false
        }
      ]);

      setIsAddingNew(false);
      setNewOption({ type: 'email', value: '' });

      toast({
        title: "Success",
        description: "Recovery option added successfully. Please verify it.",
        variant: "success"
      });
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to add recovery option",
        variant: "destructive"
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleRemoveOption = async (id: string) => {
    const option = recoveryOptions.find(opt => opt.id === id);
    if (option?.primary) {
      toast({
        title: "Error",
        description: "Cannot remove primary recovery option",
        variant: "destructive"
      });
      return;
    }

    setIsLoading(true);
    try {
      await new Promise(resolve => setTimeout(resolve, 1000));
      setRecoveryOptions(prev => prev.filter(option => option.id !== id));
      
      toast({
        title: "Success",
        description: "Recovery option removed successfully",
        variant: "success"
      });
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to remove recovery option",
        variant: "destructive"
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleSetPrimary = async (id: string) => {
    const option = recoveryOptions.find(opt => opt.id === id);
    if (!option?.verified) {
      toast({
        title: "Error",
        description: "Cannot set unverified option as primary",
        variant: "destructive"
      });
      return;
    }

    setIsLoading(true);
    try {
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      setRecoveryOptions(prev => prev.map(option => ({
        ...option,
        primary: option.id === id
      })));

      toast({
        title: "Success",
        description: "Primary recovery option updated",
        variant: "success"
      });
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to update primary recovery option",
        variant: "destructive"
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleSendVerification = async (id: string) => {
    setIsLoading(true);
    try {
      await new Promise(resolve => setTimeout(resolve, 1000));

      toast({
        title: "Success",
        description: "Verification code sent. Please check your inbox.",
        variant: "success"
      });
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to send verification code",
        variant: "destructive"
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="flex items-center gap-2">
            <LifeBuoy className="h-5 w-5" />
            Recovery Options
          </CardTitle>
          {!isAddingNew && (
            <Button
              variant="outline"
              onClick={() => setIsAddingNew(true)}
              disabled={isLoading}
            >
              <Plus className="h-4 w-4 mr-2" />
              Add New
            </Button>
          )}
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-6">
          {/* Warning Message */}
          <div className="rounded-md bg-yellow-50 p-4">
            <div className="flex">
              <AlertTriangle className="h-5 w-5 text-yellow-400" />
              <div className="ml-3">
                <h3 className="text-sm font-medium text-yellow-800">
                  Keep Your Recovery Options Up to Date
                </h3>
                <div className="mt-2 text-sm text-yellow-700">
                  <p>Recovery options help you regain access to your account if you:</p>
                  <ul className="list-disc pl-5 space-y-1 mt-2">
                    <li>Forget your password</li>
                    <li>Lose access to your 2FA device</li>
                    <li>Get locked out of your account</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>

          {/* Add New Option Form */}
          {isAddingNew && (
            <div className="space-y-4 border rounded-lg p-4">
              <div className="flex flex-col sm:flex-row gap-4">
                <select
                  value={newOption.type}
                  onChange={handleTypeChange}
                  className="px-3 py-2 border rounded-md"
                  disabled={isLoading}
                >
                  <option value="email">Email</option>
                  <option value="phone">Phone</option>
                </select>
                <input
                  type={newOption.type === 'email' ? 'email' : 'tel'}
                  value={newOption.value}
                  onChange={handleValueChange}
                  placeholder={newOption.type === 'email' ? 
                    'Enter recovery email' : 
                    'Enter recovery phone'
                  }
                  className="flex-1 px-3 py-2 border rounded-md"
                  disabled={isLoading}
                />
              </div>
              <div className="flex justify-end gap-2">
                <Button
                  variant="outline"
                  onClick={() => {
                    setIsAddingNew(false);
                    setNewOption({ type: 'email', value: '' });
                  }}
                  disabled={isLoading}
                >
                  Cancel
                </Button>
                <Button
                  onClick={handleAddOption}
                  disabled={isLoading}
                >
                  {isLoading ? (
                    <>
                      <RefreshCw className="h-4 w-4 mr-2 animate-spin" />
                      Adding...
                    </>
                  ) : (
                    'Add Option'
                  )}
                </Button>
              </div>
            </div>
          )}

          {/* Existing Options */}
          <div className="space-y-4">
            {recoveryOptions.map((option) => (
              <div
                key={option.id}
                className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 p-4 border rounded-lg"
              >
                <div className="flex items-center gap-3">
                  {option.type === 'email' ? (
                    <Mail className="h-5 w-5 text-blue-500" />
                  ) : (
                    <Phone className="h-5 w-5 text-green-500" />
                  )}
                  <div>
                    <p className="font-medium">
                      {option.value}
                      {option.primary && (
                        <span className="ml-2 text-xs bg-blue-100 text-blue-800 px-2 py-0.5 rounded-full">
                          Primary
                        </span>
                      )}
                    </p>
                    <div className="flex items-center gap-2 mt-1">
                      {option.verified ? (
                        <span className="flex items-center text-xs text-green-600">
                          <BadgeCheck className="h-3 w-3 mr-1" />
                          Verified
                        </span>
                      ) : (
                        <span className="flex items-center text-xs text-yellow-600">
                          <AlertTriangle className="h-3 w-3 mr-1" />
                          Not verified
                        </span>
                      )}
                    </div>
                  </div>
                </div>
                <div className="flex items-center gap-2 w-full sm:w-auto">
                  {!option.verified && (
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleSendVerification(option.id)}
                      disabled={isLoading}
                      className="flex-1 sm:flex-none"
                    >
                      Verify
                    </Button>
                  )}
                  {!option.primary && option.verified && (
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleSetPrimary(option.id)}
                      disabled={isLoading}
                      className="flex-1 sm:flex-none"
                    >
                      <Shield className="h-4 w-4 mr-2" />
                      Set as Primary
                    </Button>
                  )}
                  {!option.primary && (
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => handleRemoveOption(option.id)}
                      disabled={isLoading}
                      className="text-red-600 hover:text-red-700"
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  );
}