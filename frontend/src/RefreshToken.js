function RefreshToken() {
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
        const data = response;
        console.log("Data response", data);
        console.log("Token Refreshed");
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