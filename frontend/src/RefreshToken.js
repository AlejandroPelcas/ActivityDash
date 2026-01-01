function RefreshToken() {
    // Create function to handle click of button
    const handleClick = async () => {
        console.log("Clicked Refresh Token");
        try {
            const response = await fetch('http://localhost:5000/refresh-token', {
                method: "POST",
            }
        );
        const data = response.json();
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