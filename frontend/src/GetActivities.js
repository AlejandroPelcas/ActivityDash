function GetActivities() {
    const handleClick = async () => {
      try {
        const response = await fetch(
          "http://127.0.0.1:5000/activities"
        );
  
        if (!response.ok) {
          throw new Error(`HTTP error ${response.status}`);
        }
  
        const data = await response.json();
        console.log("Strava activities:", data);
      } catch (error) {
        console.error("Failed to load activities:", error);
      }
    };
  
    return (
      <button onClick={handleClick}>
        Load Activities
      </button>
    );
  }
  
  export default GetActivities;
  