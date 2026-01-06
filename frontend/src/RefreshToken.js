function RefreshToken({refreshToken, setRefreshToken}) {
    // Create function to handle click of button
    const handleClick = async () => {
        console.log("Clicked Refresh Token");
        try {
            const response = await fetch(
                "http://127.0.0.1:5000/refresh-token",
            {
                method: "POST",
            }
        );
        if (!response.ok) {
            throw new Error(`HTTP error ${response.status}`);
          }
        const data = await response.json();
        // Error check
        console.log("Data response", data);
        console.log("Token Refreshed");
        setRefreshToken(data)
        } 
        catch (error) {
            console.log("Error: Could not refresh token", error);
        }
    };

    return (
        <div>
            <button onClick={handleClick}> Refresh Token </button>
        </div>
    )
}

export default RefreshToken;