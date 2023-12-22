

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
                <button type="submit">Submit</button>
            </form>
        </div>
    );
};

export default VolunteerForm;
