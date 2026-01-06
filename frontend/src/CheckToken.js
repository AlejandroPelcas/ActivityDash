import React from "react";

function CheckToken() {
  const handleClick = async () => {
    try {
      const response = await fetch(
        "http://127.0.0.1:5000/check-token",
        {
          method: "GET", // ✅ must be GET
        }
      );

      if (!response.ok) {
        throw new Error(`HTTP error ${response.status}`);
      }

      const data = await response.json(); // ✅ parse JSON
      console.log("Token checked:", data);

      // Example usage
      if (data.has_token) {
        console.log("Token exists ✅");
      } else {
        console.log("No token found ❌");
      }

    } catch (error) {
      console.error("Error checking token:", error);
    }
  };

  return (
    <button onClick={handleClick}>
      Check Token
    </button>
  );
}

export default CheckToken;
