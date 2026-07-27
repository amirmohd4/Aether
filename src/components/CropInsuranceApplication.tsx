import { useState } from 'react';
import { Sprout, Search, CircleAlert as AlertCircle } from 'lucide-react';

const BACKEND_URL = 'https://aether-backend-zaa9.onrender.com/api';

async function directFetch<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const url = `${BACKEND_URL}${endpoint}`;
  const res = await fetch(url, { ...options, headers: { 'Content-Type': 'application/json', ...options?.headers } });
  if (!res.ok) { const err = await res.json().catch(() => ({ error: 'Request failed' })); throw new Error(err.message || `HTTP ${res.status}`); }
  return await res.json();
}

interface CropIns { insurance_id: string; farmer_name: string; crop_name: string; status: string; claim_amount: number; claim_settled_at: string | null; issued_at: string | null; }

export function CropInsuranceApplication() {
  const [ins, setIns] = useState<CropIns | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [insId, setInsId] = useState('');
  const [citizenId, setCitizenId] = useState('CIT-DEMO-001');
  const [farmerId, setFarmerId] = useState('');
  const [farmerName, setFarmerName] = useState('');
  const [cropName, setCropName] = useState('');
  const [areaAcres, setAreaAcres] = useState('');
  const [sumInsured, setSumInsured] = useState('');
  const [premiumAmount, setPremiumAmount] = useState('');
  const [season, setSeason] = useState('kharif');
  const [village, setVillage] = useState('');
  const [district, setDistrict] = useState('');
  const [state, setState] = useState('');

  const handleApply = async (e: React.FormEvent) => {
    e.preventDefault(); setLoading(true); setError('');
    try {
      const result = await directFetch<any>('/crop-insurance/apply', {
        method: 'POST', body: JSON.stringify({ citizen_id: citizenId, farmer_id: farmerId, farmer_name: farmerName, crop_name: cropName, area_acres: parseFloat(areaAcres) || 0, sum_insured: parseFloat(sumInsured) || 0, premium_amount: parseFloat(premiumAmount) || 0, season, village, district, state }),
      });
      setIns(result); setInsId(result.insurance_id); alert('✅ Crop insurance application submitted!');
    } catch (err: any) { setError(err.message); } finally { setLoading(false); }
  };

  const handleStatusCheck = async () => {
    if (!insId) { setError('Please enter an insurance ID'); return; }
    setLoading(true); setError('');
    try { const result = await directFetch<CropIns>(`/crop-insurance/status/${insId}`); setIns(result); } catch (err: any) { setError(err.message); } finally { setLoading(false); }
  };

  const getStatusColor = (status: string) => ({ applied: 'bg-yellow-100 text-yellow-800', approved: 'bg-blue-100 text-blue-800', claim_settled: 'bg-green-100 text-green-800', rejected: 'bg-red-100 text-red-800' }[status] || 'bg-gray-100 text-gray-800');

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-6">
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2"><Sprout className="w-6 h-6 text-blue-600" />Crop Insurance Application</h2>
        {error && <div className="mb-4 p-4 bg-red-100 border border-red-300 rounded-lg text-red-700"><AlertCircle className="w-5 h-5 inline mr-2" />{error}</div>}
        <form onSubmit={handleApply} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div><label className="block text-sm font-medium text-gray-700">Citizen ID *</label><input type="text" value={citizenId} onChange={(e) => setCitizenId(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" required /></div>
            <div><label className="block text-sm font-medium text-gray-700">Farmer ID</label><input type="text" value={farmerId} onChange={(e) => setFarmerId(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" /></div>
            <div><label className="block text-sm font-medium text-gray-700">Farmer Name *</label><input type="text" value={farmerName} onChange={(e) => setFarmerName(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" required /></div>
            <div><label className="block text-sm font-medium text-gray-700">Crop Name *</label><input type="text" value={cropName} onChange={(e) => setCropName(e.target.value)} placeholder="e.g., Rice, Wheat" className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" required /></div>
            <div><label className="block text-sm font-medium text-gray-700">Area (Acres)</label><input type="number" step="0.01" value={areaAcres} onChange={(e) => setAreaAcres(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" /></div>
            <div><label className="block text-sm font-medium text-gray-700">Sum Insured (₹)</label><input type="number" value={sumInsured} onChange={(e) => setSumInsured(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" /></div>
            <div><label className="block text-sm font-medium text-gray-700">Premium Amount (₹)</label><input type="number" value={premiumAmount} onChange={(e) => setPremiumAmount(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" /></div>
            <div><label className="block text-sm font-medium text-gray-700">Season *</label><select value={season} onChange={(e) => setSeason(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg"><option value="kharif">Kharif</option><option value="rabi">Rabi</option></select></div>
            <div><label className="block text-sm font-medium text-gray-700">Village</label><input type="text" value={village} onChange={(e) => setVillage(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" /></div>
            <div><label className="block text-sm font-medium text-gray-700">District</label><input type="text" value={district} onChange={(e) => setDistrict(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" /></div>
            <div><label className="block text-sm font-medium text-gray-700">State</label><input type="text" value={state} onChange={(e) => setState(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" /></div>
          </div>
          <button type="submit" disabled={loading} className="w-full py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50">{loading ? 'Submitting...' : 'Apply for Crop Insurance'}</button>
        </form>
      </div>
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h3 className="text-xl font-bold text-gray-900 mb-4">Check Insurance Status</h3>
        <div className="flex gap-3">
          <input type="text" value={insId} onChange={(e) => setInsId(e.target.value)} placeholder="Enter Insurance ID" className="flex-1 px-4 py-2 border border-gray-300 rounded-lg" />
          <button onClick={handleStatusCheck} disabled={loading} className="px-6 py-2 bg-gray-800 text-white rounded-lg hover:bg-gray-900 flex items-center gap-2"><Search className="w-4 h-4" /> Check</button>
        </div>
      </div>
      {ins && (
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h3 className="text-xl font-bold text-gray-900 mb-4">Insurance Details</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <p><span className="font-medium">Insurance ID:</span> {ins.insurance_id}</p>
            <p><span className="font-medium">Farmer:</span> {ins.farmer_name}</p>
            <p><span className="font-medium">Crop:</span> {ins.crop_name}</p>
            <p><span className="font-medium">Status:</span><span className={`ml-2 px-2 py-1 rounded text-xs ${getStatusColor(ins.status)}`}>{ins.status}</span></p>
            <p><span className="font-medium">Claim Amount:</span> ₹{ins.claim_amount}</p>
            <p><span className="font-medium">Claim Settled:</span> {ins.claim_settled_at ? new Date(ins.claim_settled_at).toLocaleDateString() : 'Not settled'}</p>
            <p><span className="font-medium">Issued At:</span> {ins.issued_at ? new Date(ins.issued_at).toLocaleDateString() : 'Not issued'}</p>
          </div>
        </div>
      )}
    </div>
  );
}
