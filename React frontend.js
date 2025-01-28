import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Apisearch = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSearchChange = (e) => {
    setSearchQuery(e.target.value);
  };

  useEffect(() => {
    const debounceTimer = setTimeout(() => {
      if (searchQuery.trim() === '') return;

      setLoading(true);
      setError(null);

      axios
        .get('http://127.0.0.1:8000/api/query/', {
          params: { query: searchQuery },
        })
        .then((response) => {
          const fetchedResults = Array.isArray(response.data.results) ? response.data.results : [];
          setResults(fetchedResults);
        })
        .catch(() => {
          setError('An error occurred while fetching results');
        })
        .finally(() => {
          setLoading(false);
        });
    }, 500);

    return () => clearTimeout(debounceTimer);
  }, [searchQuery]);

  const renderTable = () => {
    if (results.length === 0) return <p className="message">No results found</p>;

    const columns = Object.keys(results[0]);

    return (
      <table className="table">
        <thead>
          <tr>
            {columns.map((col) => (
              <th key={col}>{col}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {results.map((row) => (
            <tr key={row.id}>
              {columns.map((col) => (
                <td key={col}>
                  {col === 'supplier' && typeof row[col] === 'object' && row[col] !== null
                    ? renderSupplier(row[col])
                    : row[col]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    );
  };

  const renderSupplier = (supplier) => (
    <div className="supplier-details">
      <strong>{supplier.name}</strong>
      <br />
      <span>Contact: {supplier.contact_info}</span>
      <br />
      <span>Categories: {supplier.product_categories_offered}</span>
    </div>
  );

  return (
    <div className="container">
      <link rel="stylesheet" href="/Apisearch.css" />
      <input
        type="text"
        value={searchQuery}
        onChange={handleSearchChange}
        placeholder="Search..."
        className="search-box"
      />
      {loading && <p className="message loading">Loading...</p>}
      {error && <p className="error">{error}</p>}
      {renderTable()}
    </div>
  );
};

export default Apisearch;
