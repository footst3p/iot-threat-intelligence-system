import React, { useState } from "react";

export const Tabs = ({ defaultValue, children }) => {
  const [value, setValue] = useState(defaultValue);

  return React.Children.map(children, (child) => {
    if (child.type === TabsList) {
      return React.cloneElement(child, { value, onChange: setValue });
    } else if (child.props.value === value) {
      return child;
    }
    return null;
  });
};

export const TabsList = ({ children, value, onChange }) => {
  return (
    <div className="tabs-list">
      {React.Children.map(children, (child) =>
        React.cloneElement(child, {
          isActive: child.props.value === value,
          onClick: () => onChange(child.props.value),
        })
      )}
    </div>
  );
};

export const TabsTrigger = ({ value, onClick, isActive, children }) => {
  return (
    <button
      onClick={onClick}
      className={`tab-trigger ${isActive ? "active" : ""}`}
    >
      {children}
    </button>
  );
};

export const TabsContent = ({ children }) => {
  return <div className="tabs-content">{children}</div>;
};
