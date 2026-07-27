import { useState } from 'react';
import { Wheat, Search, CircleAlert as AlertCircle } from 'lucide-react';

const BACKEND_URL = 'https://aether-backend-zaa9.onrender.com/api';

async function directFetch<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const url = `${BACKEND_URL}${endpoint}`;
  const res = await fetch(url, { ...options, headers: { 'Content-Type': 'application/json', ...options?.headers } });
  if (!res.ok) { const err = await res.json().catch(() => ({ error: 'Request failed' })); throw new Error(err.message || `HTTP ${res.status}`); }
  return await res.json();
}

interface PDSSubsidy { subsidy_id: string; beneficiary_name: string; subsidy_type: string; amount: number; status: string; disbursed_at: string | null; }

export function PDSSubsidyApplication() {
  const [subsidy, setSubsidy] = useState<PDSSubsidy | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [subsidyId, setSubsidyId] = useState('');
  const [citizenId, setCitizenId] = useState('CIT-DEMO-001');
  const [rationCardId, setRationCardId] = useState('');
  const [beneficiaryName, setBeneficiaryName] = useState('');
  const [subsidyType, setSubsidyType] = useState('food');
  const [amount, setAmount] = useState('');
  const [bankAccount, setBankAccount] = useState('');
  const [ifscCode, setIfscCode] = useState('');

  const handleApply = async (e: React.FormEvent) => {
    e.preventDefault(); setLoading(true); setError('');
    try {
      const result = await directFetch<any>('/pds-subsidy/apply', {
        method: 'POST', body: JSON.stringify({ citizen_id: citizenId, ration_card_id: rationCardId, beneficiary_name: beneficiaryName, subsidy_type: subsidyType, amount: parseFloat(amount) || 0, bank_account: bankAccount, ifsc_code: ifscCode }),
      });
      setSubsidy(result); setSubsidyId(result.subsidy_id); alert('✅ PDS subsidy application submitted!');
    } catch (err: any) { setError(err.message); } finally { setLoading(false); }
  };

  const handleStatusCheck = async () => {
    if (!subsidyId) { setError('Please enter a subsidy ID'); return; }
    setLoading(true); setError('');
    try { const result = await directFetch<PDSSubsidy>(`/pds-subsidy/status/${subsidyId}`); setSubsidy(result); } catch (err: any) { setError(err.message); } finally { setLoading(false); }
  };

  const getStatusColor = (status: string) => ({ applied: 'bg-yellow-100 text-yellow-800', approved: 'bg-blue-100 text-blue-800', disbursed: 'bg-green-100 text-green-800', rejected: 'bg-red-100 text-red-800' }[status] || 'bg-gray-100 text-gray-800');

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-6">
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2"><Wheat className="w-6 h-6 text-blue-600" />PDS Subsidy Application</h2>
        {error && <div className="mb-4 p-4 bg-red-100 border border-red-300 rounded-lg text-red-700"><AlertCircle className="w-5 h-5 inline mr-2" />{error}</div>}
        <form onSubmit={handleApply} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div><label className="block text-sm font-medium text-gray-700">Citizen ID *</label><input type="text" value={citizenId} onChange={(e) => setCitizenId(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" required /></div>
            <div><label className="block text-sm font-medium text-gray-700">Ration Card ID *</label><input type="text" value={rationCardId} onChange={(e) => setRationCardId(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" required /></div>
            <div><label className="block text-sm font-medium text-gray-700">Beneficiary Name *</label><input type="text" value={beneficiaryName} onChange={(e) => setBeneficiaryName(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" required /></div>
            <div><label className="block text-sm font-medium text-gray-700">Subsidy Type *</label><select value={subsidyType} onChange={(e) => setSubsidyType(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg"><option value="food">Food</option><option value="lpg">LPG</option><option value="fertilizer">Fertilizer</option></select></div>
            <div><label className="block text-sm font-medium text-gray-700">Amount (₹)</label><input type="number" value={amount} onChange={(e) => setAmount(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" /></div>
            <div><label className="block text-sm font-medium text-gray-700">Bank Account No.</label><input type="text" value={bankAccount} onChange={(e) => setBankAccount(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" /></div>
            <div><label className="block text-sm font-medium text-gray-700">IFSC Code</label><input type="text" value={ifscCode} onChange={(e) => setIfscCode(e.target.value)} placeholder="SBIN0001234" className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" /></div>
          </div>
          <button type="submit" disabled={loading} className="w-full py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50">{loading ? 'Submitting...' : 'Apply for PDS Subsidy'}</button>
        </form>
      </div>
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h3 className="text-xl font-bold text-gray-900 mb-4">Check Subsidy Status</h3>
        <div className="flex gap-3">
          <input type="text" value={subsidyId} onChange={(e) => setSubsidyId(e.target.value)} placeholder="Enter Subsidy ID" className="flex-1 px-4 py-2 border border-gray-300 rounded-lg" />
          <button onClick={handleStatusCheck} disabled={loading} className="px-6 py-2 bg-gray-800 text-white rounded-lg hover:bg-gray-900 flex items-center gap-2"><Search className="w-4 h-4" /> Check</button>
        </div>
      </div>
      {subsidy && (
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h3 className="text-xl font-bold text-gray-900 mb-4">Subsidy Details</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <p><span className="font-medium">Subsidy ID:</span> {subsidy.subsidy_id}</p>
            <p><span className="font-medium">Beneficiary:</span> {subsidy.beneficiary_name}</p>
            <p><span className="font-medium">Type:</span> {subsidy.subsidy_type}</p>
            <p><span className="font-medium">Amount:</span> ₹{subsidy.amount}</p>
            <p><span className="font-medium">Status:</span><span className={`ml-2 px-2 py-1 rounded text-xs ${getStatusColor(subsidy.status)}`}>{subsidy.status}</span></p>
            <p><span className="font-medium">Disbursed At:</span> {subsidy.disbursed_at ? new Date(subsidy.disbursed_at).toLocaleDateString() : 'Not disbursed'}</p>
          </div>
        </div>
      )}
    </div>
  );
}
