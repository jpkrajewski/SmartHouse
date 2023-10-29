import React from "react";

const Button = () => {
  const bootstrapButtonClases = [
    "btn-primary",
    "btn-secondary",
    "btn-success",
    "btn-danger",
    "btn-warning",
    "btn-info",
    "btn-light",
    "btn-dark",
    "btn-link",
  ];

  return <>
    <div className="btn-group" role="group" aria-label="Basic example">
      {bootstrapButtonClases.map((buttonClass) => {
        return <button type="button" className={`btn ${buttonClass}`} onClick={() => console.log(buttonClass)}>{buttonClass}</button>;
      })}
    </div>
  </>;
};

export default Button;
