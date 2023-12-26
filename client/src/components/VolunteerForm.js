

import React, { useState } from 'react';
import './VolunteerForm.scss';

const VolunteerForm = () => {
    const [formData, setFormData] = useState({
        fieldName: '',
        workDescription: '',
        contactInfo:''
    });

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        console.log(formData);
    };

    let register = (event) => {
        event.preventDefault();

        setFormFilled(false);
        setUsernameTakenError(false);

        if (password !== passwordRepeat) {
            setPasswordsError(true);
            return;
        }

    fetch(`http://localhost:5000/registraion`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
        body: JSON.stringify({"yehuda", "1234", name, "06543", "qhdhggv"}),
    })
        .then((response) => response.json())
        .then((data) => {
            // Handle the response data
            if (data.message === "Username taken") setUsernameTakenError(true);

            if (data.message !== "Register successful") return;

            setTimeout(() => setFormFilled(true), 1000);
        })
        .catch((error) => {
            // Handle any errors
            console.error(error);
        });
};

    return (
        <div className="volunteer-form-container">
            <form className="volunteer-form" onSubmit={handleSubmit}>
                <h1>Application for Agricultural Assistance</h1>
                <div className="form-group">
                    <label htmlFor="fieldName">Field Name</label>
                    <input 
                        type="text" 
                        id="fieldName" 
                        name="fieldName" 
                        value={formData.fieldName} 
                        onChange={handleChange} 
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="workDescription">Work Description</label>
                    <textarea 
                        id="workDescription" 
                        name="workDescription" 
                        value={formData.workDescription} 
                        onChange={handleChange}
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="contactInfo">Contact info</label>
                    <textarea 
                        id="contactInfo" 
                        name="contactInfo" 
                        value={formData.contactInfo} 
                        onChange={handleChange}
                    />
                </div>
                <button type="submit" onClick={register}>Submit</button>
            </form>
        </div>
    );
};

export default VolunteerForm;
