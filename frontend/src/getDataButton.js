function GetDataButton() {
    const handleClick =  async () => {
        const response = await 
        fetch("http://127.0.0.1:5000/get-data",);
    };
    return (
      <button onClick={handleClick()}>
        clickme
      </button>
    );
  }
  
  export default GetDataButton;
  