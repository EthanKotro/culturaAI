import React, { useEffect, useState } from 'react';
import { TfiEmail } from "react-icons/tfi";
import { CiLocationOn } from "react-icons/ci";
import axios from 'axios';

const Contact = () => {
  const [message, setMessage] = useState('');

  useEffect(() => {
    const fetchMessages = async () => {
      try {
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/contacts/`);
        setMessage(response.data);
      } catch (error) {
        console.error('Error fetching data:', error);
        setMessage('Failed to load message. Please try again later.');
      }
    };
    fetchMessages();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const form = e.target;
    const data = {
      name: form[0].value,
      email: form[1].value,
      phone_number: form[2].value,
      message: form[3].value,
      consent: form[4].checked
    };
    try {
      await axios.post(`${import.meta.env.VITE_API_URL}/contacts/`, data);
      setMessage('Message sent successfully!');
      form.reset();
    } catch (error) {
      console.error('Error posting data:', error);
      setMessage('Failed to send message. Please try again later.');
    }
  };

  return (
    <section id="contact" className="contact-wrapper">
      <div className="contact-container border-b border-red-500 bg-[#342603]/90 p-6 text-white">
        <div className="flex flex-col p-6 md:p-12">
          <h1 className="text-green-500 font-semibold">Get in touch</h1>

          <div className="flex flex-col md:flex-row gap-8">
            {/* Form */}
            <div className="flex flex-col md:w-1/2 space-y-4">
              <h2 className="font-bold text-2xl md:text-4xl">We'd love to hear from you!</h2>
              <form onSubmit={handleSubmit} className="space-y-3">
                <label>Name <span className="text-red-500">*</span></label>
                <input type="text" required placeholder="John Doe" className="p-2 w-full rounded border border-white" />

                <label>Email <span className="text-red-500">*</span></label>
                <input type="email" required placeholder="email@website.com" className="p-2 w-full rounded border border-white" />

                <label>Phone Number <span className="text-red-500">*</span></label>
                <input type="tel" required placeholder="+254 7000 00000" className="p-2 w-full rounded border border-white" />

                <label>Message</label>
                <textarea placeholder="Your Message" className="p-2 w-full rounded border border-white h-32"></textarea>

                <label className="flex items-start gap-2">
                  <input type="checkbox" required />
                  <span>I allow this website to store my submission so they respond to my inquiry. <span className="text-red-500">*</span></span>
                </label>

                <button type="submit" className="bg-green-500 text-white p-2 rounded w-full hover:bg-green-600">SUBMIT</button>
              </form>
            </div>

            {/* Contact Info */}
            <div className="bg-[#342603]/70 rounded-sm p-6 md:w-1/2">
              <h1 className="font-bold mb-2">Contact Info</h1>
              <div className="flex items-center gap-2 mb-4">
                <TfiEmail size={20} />
                <p className="underline cursor-pointer hover:text-green-500">culturaai@gmail.com</p>
              </div>

              <h1 className="font-bold">Location</h1>
              <div className="flex items-center gap-2 mb-4">
                <CiLocationOn size={20} />
                <p className="underline cursor-pointer hover:text-green-500">Nairobi 30, KE</p>
              </div>

              <h1 className="font-bold">Hours</h1>
              <table className="text-sm mt-2">
                <tbody>
                  {[
                    ['Monday – Friday', '9:00 AM – 10:00 PM'],
                    ['Saturday', '9:00 AM – 6:00 PM'],
                    ['Sunday', '9:00 AM – 12:00 PM'],
                  ].map(([day, time], i) => (
                    <tr key={i}>
                      <td className="pr-4">{day}</td>
                      <td>{time}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Messages Display */}
          <div className="mt-10 bg-[#2c2002] p-4 rounded w-full">
            {Array.isArray(message) && message.length > 0 ? (
              message.map((msg, index) => (
                <div key={msg.id || index} className="mb-4 border-b border-white/20 pb-2">
                  <p><strong>Name:</strong> {msg.name}</p>
                  <p><strong>Email:</strong> {msg.email}</p>
                  <p><strong>Phone:</strong> {msg.phone_number}</p>
                  <p><strong>Message:</strong> {msg.message}</p>
                </div>
              ))
            ) : (
              <p className="text-lg">{message}</p>
            )}
          </div>
        </div>
      </div>
    </section>
  );
};

export default Contact;
