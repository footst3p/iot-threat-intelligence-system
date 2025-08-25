import React from "react";

export const Table = ({ children }) => {
  return <table className="w-full border-collapse">{children}</table>;
};

export const TableHead = ({ children }) => {
  return <thead className="bg-gray-100">{children}</thead>;
};

export const TableBody = ({ children }) => {
  return <tbody>{children}</tbody>;
};

export const TableRow = ({ children }) => {
  return <tr className="border-b">{children}</tr>;
};

export const TableCell = ({ children, className = "" }) => {
  return <td className={`p-2 text-sm ${className}`}>{children}</td>;
};

export const TableHeader = ({ children }) => {
  return <tr className="text-left">{children}</tr>;
};
