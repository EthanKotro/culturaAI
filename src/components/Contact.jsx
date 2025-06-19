import React from 'react'
import { TfiEmail } from "react-icons/tfi";
import { CiLocationOn } from "react-icons/ci";

const Contact = () => {
  return (
    <div className='contact-wrapper' id='contact'>
    <div className="contact-container border-b-1 border-b-red-500 bg-[#342603]/90 p-6 flex flex-col text-white justify-start">
        <div className="flex flex-col p-12">
            <h1 className='text-green-500 font-semibold'>Get in touch</h1>
            <div className='flex'>
                <div className='flex flex-col w-[50%] space-y-2 p-6'>
                    <h2 className='font-bold text-4xl text-wrap'>We'd love to hear from you!</h2>
                    <form className='space-y-4'>
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
        </div>
    </div>
    </div>
  )
}

export default Contact