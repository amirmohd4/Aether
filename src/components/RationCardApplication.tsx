import { useState } from 'react';
import { Package, Search, CircleAlert as AlertCircle } from 'lucide-react';

const BACKEND_URL = 'https://aether-backend-zaa9.onrender.com/api';

async function directFetch<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const url = `${BACKEND_URL}${endpoint}`;
  const res = await fetch(url, { ...options, headers: { 'Content-Type': 'application/json', ...options?.headers } });
  if (!res.ok) { const err = await res.json().catch(() => ({ error: 'Request failed' })); throw new Error(err.message || `HTTP ${res.status}`); }
  return await res.json();
}

interface RationCard { card_id: string; head_of_family: string; card_type: string; status: string; issued_at: string | null; expires_at: string | null; }

export function RationCardApplication() {
  const [card, setCard] = useState<RationCard | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [cardId, setCardId] = useState('');
  const [citizenId, setCitizenId] = useState('CIT-DEMO-001');
  const [headOfFamily, setHeadOfFamily] = useState('');
  const [cardType, setCardType] = useState('');
  const [address, setAddress] = useState('');
  const [district, setDistrict] = useState('');
  const [state, setState] = useState('');
  const [members, setMembers] = useState('');
  const [annualIncome, setAnnualIncome] = useState('');

  const handleApply = async (e: React.FormEvent) => {
    e.preventDefault(); setLoading(true); setError('');
    try {
      const result = await directFetch<any>('/ration-card/apply', {
        method: 'POST', body: JSON.stringify({ citizen_id: citizenId, head_of_family: headOfFamily, card_type: cardType, address, district, state, members: members.split(',').map(m => m.trim()).filter(Boolean), annual_income: parseFloat(annualIncome) || 0 }),
      });
      setCard(result); setCardId(result.card_id); alert('✅ Ration card application submitted!');
    } catch (err: any) { setError(err.message); } finally { setLoading(false); }
  };

  const handleStatusCheck = async () => {
    if (!cardId) { setError('Please enter a card ID'); return; }
    setLoading(true); setError('');
    try { const result = await directFetch<RationCard>(`/ration-card/status/${cardId}`); setCard(result); } catch (err: any) { setError(err.message); } finally { setLoading(false); }
  };

  const getStatusColor = (status: string) => ({ applied: 'bg-yellow-100 text-yellow-800', approved: 'bg-green-100 text-green-800', rejected: 'bg-red-100 text-red-800' }[status] || 'bg-gray-100 text-gray-800');

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-6">
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2"><Package className="w-6 h-6 text-blue-600" />Ration Card Application</h2>
        {error && <div className="mb-4 p-4 bg-red-100 border border-red-300 rounded-lg text-red-700"><AlertCircle className="w-5 h-5 inline mr-2" />{error}</div>}
        <form onSubmit={handleApply} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div><label className="block text-sm font-medium text-gray-700">Citizen ID *</label><input type="text" value={citizenId} onChange={(e) => setCitizenId(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" required /></div>
            <div><label className="block text-sm font-medium text-gray-700">Head of Family *</label><input type="text" value={headOfFamily} onChange={(e) => setHeadOfFamily(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" required /></div>
            <div><label className="block text-sm font-medium text-gray-700">Card Type *</label><select value={cardType} onChange={(e) => setCardType(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" required><option value="">Select</option><option value="AAY">AAY (Antyodaya Anna Yojana)</option><option value="BPL">BPL (Below Poverty Line)</option><option value="APL">APL (Above Poverty Line)</option></select></div>
            <div><label className="block text-sm font-medium text-gray-700">Annual Income (₹)</label><input type="number" value={annualIncome} onChange={(e) => setAnnualIncome(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" /></div>
            <div><label className="block text-sm font-medium text-gray-700">District</label><input type="text" value={district} onChange={(e) => setDistrict(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" /></div>
            <div><label className="block text-sm font-medium text-gray-700">State</label><input type="text" value={state} onChange={(e) => setState(e.target.value)} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" /></div>
            <div className="md:col-span-2"><label className="block text-sm font-medium text-gray-700">Family Members (comma separated)</label><input type="text" value={members} onChange={(e) => setMembers(e.target.value)} placeholder="John, Jane, Child1" className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" /></div>
            <div className="md:col-span-2"><label className="block text-sm font-medium text-gray-700">Address</label><textarea value={address} onChange={(e) => setAddress(e.target.value)} rows={2} className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg" /></div>
          </div>
          <button type="submit" disabled={loading} className="w-full py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50">{loading ? 'Submitting...' : 'Apply for Ration Card'}</button>
        </form>
      </div>
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h3 className="text-xl font-bold text-gray-900 mb-4">Check Card Status</h3>
        <div className="flex gap-3">
          <input type="text" value={cardId} onChange={(e) => setCardId(e.target.value)} placeholder="Enter Card ID" className="flex-1 px-4 py-2 border border-gray-300 rounded-lg" />
          <button onClick={handleStatusCheck} disabled={loading} className="px-6 py-2 bg-gray-800 text-white rounded-lg hover:bg-gray-900 flex items-center gap-2"><Search className="w-4 h-4" /> Check</button>
        </div>
      </div>
      {card && (
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h3 className="text-xl font-bold text-gray-900 mb-4">Card Details</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <p><span className="font-medium">Card ID:</span> {card.card_id}</p>
            <p><span className="font-medium">Head of Family:</span> {card.head_of_family}</p>
            <p><span className="font-medium">Card Type:</span> {card.card_type}</p>
            <p><span className="font-medium">Status:</span><span className={`ml-2 px-2 py-1 rounded text-xs ${getStatusColor(card.status)}`}>{card.status}</span></p>
            <p><span className="font-medium">Issued At:</span> {card.issued_at ? new Date(card.issued_at).toLocaleDateString() : 'Not issued'}</p>
            <p><span className="font-medium">Expires At:</span> {card.expires_at ? new Date(card.expires_at).toLocaleDateString() : 'N/A'}</p>
          </div>
        </div>
      )}
    </div>
  );
}
