import { useState } from 'react';
import { supabase, type Application } from '../lib/supabase';
import { FileText, CircleCheck as CheckCircle, Clock, CircleAlert as AlertCircle } from 'lucide-react';

type Props = {
  selectedState: string;
};

export function CitizenPortal({ selectedState }: Props) {
  const [formData, setFormData] = useState({
    citizen_name: '',
    aadhaar_number: '',
    property_address: '',
    district: '',
  });
  const [submittedApplication, setSubmittedApplication] = useState<Application | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    setError(null);

    try {
      const { data, error: dbError } = await supabase
        .from('applications')
        .insert([
          {
            ...formData,
            state: selectedState,
            status: 'submitted',
            department: 'Land Records',
          },
        ])
        .select()
        .single();

      if (dbError) throw dbError;

      setSubmittedApplication(data);
      setFormData({
        citizen_name: '',
        aadhaar_number: '',
        property_address: '',
        district: '',
      });
    } catch (err) {
      setError('Failed to submit application. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const statusSteps = [
    { label: 'Submitted', value: 'submitted', icon: FileText },
    { label: 'Verified', value: 'verified', icon: CheckCircle },
    { label: 'Approved', value: 'approved', icon: CheckCircle },
    { label: 'Completed', value: 'completed', icon: CheckCircle },
  ];

  const getStatusIndex = (status: string) => {
    return statusSteps.findIndex((step) => step.value === status);
  };

  if (submittedApplication) {
    const currentIndex = getStatusIndex(submittedApplication.status);

    return (
      <div className="bg-white rounded-lg shadow-md p-8">
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-green-100 rounded-full mb-4">
            <CheckCircle className="w-8 h-8 text-green-600" />
          </div>
          <h2 className="text-2xl font-bold text-gray-800 mb-2">Application Submitted Successfully!</h2>
          <p className="text-gray-600">Application ID: {submittedApplication.id.slice(0, 8).toUpperCase()}</p>
        </div>

        <div className="mb-8">
          <h3 className="font-semibold text-gray-800 mb-4">Application Status Tracker</h3>
          <div className="relative">
            <div className="absolute top-5 left-0 right-0 h-1 bg-gray-200">
              <div
                className="h-full bg-blue-600 transition-all duration-500"
                style={{ width: `${(currentIndex / (statusSteps.length - 1)) * 100}%` }}
              ></div>
            </div>
            <div className="relative flex justify-between">
              {statusSteps.map((step, index) => {
                const Icon = step.icon;
                const isCompleted = index <= currentIndex;
                const isCurrent = index === currentIndex;

                return (
                  <div key={step.value} className="flex flex-col items-center">
                    <div
                      className={`w-10 h-10 rounded-full flex items-center justify-center mb-2 transition-all ${
                        isCompleted
                          ? 'bg-blue-600 text-white'
                          : 'bg-gray-200 text-gray-400'
                      } ${isCurrent ? 'ring-4 ring-blue-200' : ''}`}
                    >
                      <Icon className="w-5 h-5" />
                    </div>
                    <span
                      className={`text-sm font-medium ${
                        isCompleted ? 'text-blue-600' : 'text-gray-400'
                      }`}
                    >
                      {step.label}
                    </span>
                  </div>
                );
              })}
            </div>
          </div>
        </div>

        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
          <div className="flex items-start">
            <Clock className="w-5 h-5 text-blue-600 mr-3 mt-0.5" />
            <div>
              <p className="font-medium text-blue-900">Processing Time</p>
              <p className="text-sm text-blue-700">Estimated completion: 3-5 business days</p>
            </div>
          </div>
        </div>

        <button
          onClick={() => setSubmittedApplication(null)}
          className="w-full bg-blue-600 text-white py-3 rounded-lg font-medium hover:bg-blue-700 transition-colors"
        >
          Submit Another Application
        </button>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-8">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">Property Registration Application</h2>

      {error && (
        <div className="mb-6 bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-red-800 text-sm">{error}</p>
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Full Name <span className="text-red-500">*</span>
          </label>
          <input
            type="text"
            required
            value={formData.citizen_name}
            onChange={(e) => setFormData({ ...formData, citizen_name: e.target.value })}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="Enter your full name"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Aadhaar Number <span className="text-red-500">*</span>
          </label>
          <input
            type="text"
            required
            value={formData.aadhaar_number}
            onChange={(e) => setFormData({ ...formData, aadhaar_number: e.target.value })}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="XXXX-XXXX-XXXX"
            pattern="[0-9]{4}-[0-9]{4}-[0-9]{4}"
          />
          <p className="text-xs text-gray-500 mt-1">Format: 1234-5678-9012</p>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Property Address <span className="text-red-500">*</span>
          </label>
          <textarea
            required
            value={formData.property_address}
            onChange={(e) => setFormData({ ...formData, property_address: e.target.value })}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            rows={3}
            placeholder="Enter complete property address"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            District <span className="text-red-500">*</span>
          </label>
          <input
            type="text"
            required
            value={formData.district}
            onChange={(e) => setFormData({ ...formData, district: e.target.value })}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="Enter district name"
          />
        </div>

        <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
          <div className="flex items-start">
            <AlertCircle className="w-5 h-5 text-gray-600 mr-3 mt-0.5" />
            <div className="text-sm text-gray-600">
              <p className="font-medium mb-1">Required Documents (to be uploaded later):</p>
              <ul className="list-disc list-inside space-y-1">
                <li>Property ownership documents</li>
                <li>Aadhaar card copy</li>
                <li>Sale deed or transfer documents</li>
              </ul>
            </div>
          </div>
        </div>

        <button
          type="submit"
          disabled={isSubmitting}
          className="w-full bg-blue-600 text-white py-3 rounded-lg font-medium hover:bg-blue-700 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed"
        >
          {isSubmitting ? 'Submitting...' : 'Submit Application'}
        </button>
      </form>
    </div>
  );
}
