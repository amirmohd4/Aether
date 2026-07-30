import React, { useState } from 'react';
import { Search } from 'lucide-react';

interface SearchBoxProps {
  onSearch: (query: string) => void;
}

export const SearchBox: React.FC<SearchBoxProps> = ({ onSearch }) => {
  const [query, setQuery] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSearch(query.trim());
  };

  return (
    <div className="w-full">
      <form onSubmit={handleSubmit} className="relative w-full">
        <div className="relative bg-white border border-slate-300 rounded-2xl shadow-lg flex items-center p-1.5 focus-within:border-[#1a365d] focus-within:ring-2 focus-within:ring-[#1a365d]/20 transition-all">
          <input
            id="input-service-search"
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="What do you need help with?"
            className="w-full bg-transparent pl-4 pr-14 py-3 text-slate-900 text-base placeholder-slate-400 focus:outline-none"
            autoFocus
          />
          <button
            id="btn-search-icon"
            type="submit"
            className="absolute right-2.5 p-2.5 rounded-xl bg-[#1a365d] hover:bg-[#122847] text-white transition-all shadow-sm flex items-center justify-center cursor-pointer"
            title="Search"
          >
            <Search className="w-5 h-5" />
          </button>
        </div>
      </form>
    </div>
  );
};
