import React, { useEffect, useState } from 'react'
import { TfiEmail } from "react-icons/tfi";
import { CiLocationOn } from "react-icons/ci";
import axios from 'axios';

const Contact = () => {

    const [message, setMessage] = useState('');

    useEffect(() => async () => {

        console.log(import.meta.env.VITE_API_URL);
        try {
            const response = await axios.get(`${import.meta.env.VITE_API_URL}/contacts/`);
            console.log("Backend Response:", response);
            setMessage(response.data);
        } catch (error) {
         console.error('Error fetching data:', error);
         setMessage('Failed to load message. Please try again later.');   
        }
        
        const handleSubmit = async (e) => { // handle form submission
            e.preventDefault(); // prevent default form behavior
            const form = e.target; // get the form element
            const data = { // collect form data
                name: form[0].value, // get name input value
                email: form[1].value, // get email input value
                phone_number: form[2].value, // get phone number input value
                message: form[3].value, // get message textarea value
                consent: form[4].checked // get checkbox value
            };
            try {
                const response = await axios.post(`${import.meta.env.VITE_API_URL}/contacts/`, data); // send POST request
                setMessage('Message sent successfully!'); // update message state on success
                form.reset(); // reset form fields
            } catch (error) {
                setMessage('Failed to send message. Please try again later.'); // update message state on error
                console.error('Error posting data:', error); // log error
            }
        };

        // Add this handler to the form element in the JSX: onSubmit={handleSubmit}

    }, [])

  return (
    <div className='contact-wrapper' id='contact'>
    <div className="contact-container border-b-1 border-b-red-500 bg-[#342603]/90 p-6 flex flex-col text-white justify-start">
        <div className="flex flex-col p-6 md:p-12">
            <h1 className='text-green-500 font-semibold'>Get in touch</h1>
            <div className='flex max-sm:flex-col'>
                <div className='flex flex-col w-[50%] space-y-2 p-3 ps-0 md:p-6'>
                    <h2 className='font-bold text-2xl md:text-4xl text-nowrap'>We'd love to hear from you!</h2>
                    <form className='md:space-y-4 space-y-2 w-full' onSubmit={handleSubmit}>
                        <label htmlFor="">Name <span className='text-red-500'>*</span></label>
                        <input type="text" placeholder="John Doe" className='p-2 w-full rounded border-1 border-white' />
                        <label htmlFor="">Email address <span className='text-red-500'>*</span></label>
                        <input type="email" placeholder="email@website.com" className='p-2 w-full rounded border-1 border-white' />
                        <label htmlFor="">Phone Number <span className='text-red-500'>*</span></label>
                        <input type="tel" placeholder="+254 7000 00000" className='p-2 w-full rounded border-1 border-white' />
                        <label htmlFor="">Message</label>
                        <textarea placeholder="Your Message" className='p-2 w-full rounded border-1 border-white h-32'></textarea>
                        <input type="checkbox" />
                        <span className='ps-1'>I allow this website to store my submission so they respond to my inquiry. <span className='text-red-500'>*</span></span>
                        <br />
                        <button type="submit" className='bg-green-500 text-white p-2 rounded w-full'>SUBMIT</button>
                    </form>
                </div>
                <div className='flex flex-col justify-start p-2 pt-12 mt-6 bg-[#342603]/70 rounded-sm w-[50%] h-[27rem]'>
                    <h1 className='font-bold'>Get in touch</h1>
                    <div className="flex p-2 space-x-2 items-center">
                        <TfiEmail size={20} />
                        <p className='underline cursor-pointer hover:text-green-500'>culturaai@gmail.com</p>
                    </div>
                    <h1 className='font-bold'>Location</h1>
                    <div className="flex p-2 space-x-2 items-center">
                        <CiLocationOn size={20} />
                        <p className='underline cursor-pointer hover:text-green-500'>Nairobi 30, KE</p>
                    </div>
                    <h1 className='font-bold ps-1'>Hours</h1>
                    <table className='p-4 m-4'>
                        <tbody>
                            <tr>
                                <td>Monday</td>
                                <td>9:00 AM - 10:00 PM</td>
                            </tr>
                            <tr>
                                <td>Tuesday</td>
                                <td>9:00 AM - 10:00 PM</td>
                            </tr>
                            <tr>
                                <td>Wednesday</td>
                                <td>9:00 AM - 10:00 PM</td>
                            </tr>
                            <tr>
                                <td>Thursday</td>
                                <td>9:00 AM - 10:00 PM</td>
                            </tr>
                            <tr>
                                <td>Friday</td>
                                <td>9:00 AM - 10:00 PM</td>
                            </tr>
                            <tr>
                                <td>Saturday</td>
                                <td>9:00 AM - 6:00 PM</td>
                            </tr>
                            <tr>
                                <td>Sunday</td>
                                <td>9:00 AM - 12:00 PM</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
            <div className='flex flex-col justify-center items-center p-6 mt-6 bg-[#342603]/40 rounded-sm'>
                {/* {message.map((msg, index) => (
                    <p key={index} className='text-lg text-white mt-4'>{msg}</p>))} */}
                {Array.isArray(message) && message.length > 0 ? (
                message.map((msg, index) => (
                    <div key={msg.id} className='text-white p-4 bg-[#2c2002] rounded mb-2 w-full'>
                    <p><strong>Name:</strong> {msg.name}</p>
                    <p><strong>Email:</strong> {msg.email}</p>
                    <p><strong>Phone:</strong> {msg.phone_number}</p>
                    <p><strong>Message:</strong> {msg.message}</p>
                    </div>
                ))
                ) : (
                <p className='text-lg text-white mt-4'>{message}</p>  // fallback for error string
                )}
            </div>
        </div>
    </div>
    </div>
  )
}

export default Contact