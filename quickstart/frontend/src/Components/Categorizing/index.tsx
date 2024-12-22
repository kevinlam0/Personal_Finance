import React, { useState } from "react";
const serverUrl = "http://127.0.0.1:8000"

type Transaction = {
    ID: number,
    Datetime: string, 
    Note: string,
    From: string,
    To: string,
    Amount: number
}
const Transaction = () => {
    const [transactions, setTransactions] = useState<Transaction[] | null>(null);
    const getData = async () => {
        console.log("Making a fetch call")
        const response = await fetch(serverUrl + "/api/hello")
        const data = await response.json()
        setTransactions(data)
    }
    return (
        <>
            <button onClick={getData}>Hello</button>
            {transactions && (
                <ul>
                {transactions.map(transaction => (
                    <li key={transaction.ID}>
                    <p><strong>Date:</strong> {transaction.Datetime}</p>
                    <p><strong>Note:</strong> {transaction.Note}</p>
                    <p><strong>From:</strong> {transaction.From}</p>
                    <p><strong>To:</strong> {transaction.To}</p>
                    <p><strong>Amount:</strong> {transaction.Amount}</p>
                    <hr />
                    </li>
                ))}
                </ul>
            )}
        </>
        )
    }
export default Transaction