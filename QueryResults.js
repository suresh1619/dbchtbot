import React, { useState, useEffect } from "react";
import axios from "axios";

const QueryResults = () => {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [columnTitles, setColumnTitles] = useState([]);

  const handleQueryChange = (e) => {
    setQuery(e.target.value);
  };

  const handleSearch = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.get(
        `http://127.0.0.1:8000/api/query/?query=${encodeURIComponent(query)}`
      );
      if (response.data) {
        setResults(response.data.results || []);
        setColumnTitles(response.data.column_titles || []);
      }
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  return (
    <div style={{ margin: "20px", fontFamily: "Arial, sans-serif", lineHeight: "1.6", color: "#333" }}>
      <h1 style={{ color: "#0056b3" }}>AI Query Results</h1>
      <form onSubmit={handleSearch} style={{ marginBottom: "20px" }}>
        <input
          type="text"
          value={query}
          onChange={handleQueryChange}
          placeholder="Enter your query"
          style={{
            width: "300px",
            padding: "8px",
            marginRight: "10px",
            border: "1px solid #ccc",
            borderRadius: "4px",
          }}
        />
        <button
          type="submit"
          style={{
            padding: "8px 16px",
            backgroundColor: "#0056b3",
            color: "white",
            border: "none",
            borderRadius: "4px",
            cursor: "pointer",
          }}
          onMouseOver={(e) => (e.target.style.backgroundColor = "#004099")}
          onMouseOut={(e) => (e.target.style.backgroundColor = "#0056b3")}
        >
          Search
        </button>
      </form>

      {query && (
        <>
          <h2 style={{ color: "#0056b3" }}>Results for "{query}":</h2>
          {results.length > 0 ? (
            <table
              style={{
                width: "100%",
                borderCollapse: "collapse",
                marginTop: "20px",
              }}
            >
              <thead>
                <tr>
                  {columnTitles.map((title, index) => (
                    <th
                      key={index}
                      style={{
                        border: "1px solid #ddd",
                        backgroundColor: "#f4f4f4",
                        color: "#333",
                        padding: "12px",
                        textAlign: "left",
                      }}
                    >
                      {title}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {results.map((result, rowIndex) => (
                  <tr
                    key={rowIndex}
                    style={rowIndex % 2 === 0 ? { backgroundColor: "#f9f9f9" } : {}}
                    onMouseOver={(e) => (e.currentTarget.style.backgroundColor = "#f1f1f1")}
                    onMouseOut={(e) => (e.currentTarget.style.backgroundColor = rowIndex % 2 === 0 ? "#f9f9f9" : "")}
                  >
                    {columnTitles.map((title, colIndex) => (
                      <td
                        key={colIndex}
                        style={{
                          border: "1px solid #ddd",
                          padding: "12px",
                          textAlign: "left",
                        }}
                      >
                        {result[title] || "N/A"}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <p style={{ color: "#666" }}>No results found for the query.</p>
          )}
        </>
      )}
    </div>
  );
};

export default QueryResults;
