import React, { useState } from "react";
const serverUrl = "http://127.0.0.1:8000"
const Transaction = () => {
    const [transactions, setTransactions] = useState([]);
    const getData = async () => {
        console.log("Making a fetch call")
        const response = await fetch(serverUrl + "/api/hello")
        const data = await response.json()
        console.log(data)

    }
    return (
        <>
            <button onClick={getData}>Hello</button>
        </>
    )
}

export default Transaction