import React, {useState} from "react";
import './index.scss';
export const CreateCategories = () => {
  const [input, setInput] = useState<string>("");
  const [finishedInput, setFinishedInput] = useState<boolean>(true);
  const [listOfInput, setListOfInput] = useState<string[]>([]);
  const [createExactly, setCreateExactly] = useState<boolean>(false);

  const handleChange = (e: React.FormEvent<HTMLInputElement>) => {
    setInput(e.currentTarget.value)
  } 

  const handleSubmit = () => {
    setListOfInput([...listOfInput, input])
    setInput("")
    console.log(listOfInput)
  }

  const handleFinished = async () => {
    const response = await fetch("/api/create_categories", {
      method: "POST",
      headers: {
        'Accept': 'application/json',
        "Content-Type": "application/json", // Specify content type
      },
      body: JSON.stringify({
        labels: listOfInput
      })
    })
  }

  return (
    <div className="createContainer">
      <h4>Enter your custom category:</h4>
      <input name="labelInput" value={input} onChange={handleChange}/>
      <button className="submit-btn" onClick={handleSubmit} disabled={input===""}>Submit</button>
      <button className="finished-btn" onClick={handleFinished} disabled={listOfInput.length < 1}>Finish</button>
    </div>
  ) 
}
