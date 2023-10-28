import React, { useState } from "react";
import axios from 'axios';
import {useNavigate} from "react-router-dom";
 
export default function RegisterPage(){
 
    const [email,setEmail] = useState('');
    const [password,setPassword] = useState('');
   
    const navigate = useNavigate();
     
    const registerUser = () => {
        axios.post('http://127.0.0.1:5000/signup', {
            email: email,
            password: password
        })
        .then(function (response) {
            console.log(response);
            alert("You have successfully created an account!")
            navigate("/");
        })
        .catch(function (error) {
            console.log(error, 'error');
            if (error.response.status === 401) {
                alert("Invalid credentials");
            }
        });
    };
     
    let imgs = [
      'https://img.freepik.com/free-vector/software-integration-concept-illustration_114360-7277.jpg?w=826&t=st=1697856849~exp=1697857449~hmac=4513d462e00ae75bfb9f143c4fdae1ac04bc283eb19bb792107a48bd8e30ef2d',
    ];
     
  return (
    <div>
        <div className="container h-100"
         style={{

                border: "1px solid #ccc", 
                borderRadius: "10px", 
                boxShadow: "0px 0px 10px rgba(0, 0, 0, 0.5)", 
                padding: "100px",
              }}>

          <div className="container-fluid h-custom">
            <div className="row d-flex justify-content-center align-items-center h-100">
              <div className="col-md-8 col-lg-6 col-xl-4 offset-xl-1">
                <form>
                  <div className="d-flex flex-row align-items-center justify-content-center justify-content-lg-start">
                    <p className="fs-2 fw-bolder">Create Your Account</p>
                  </div>
 
                  <div className="form-outline mb-4">
                    <label className="form-label" for="form3Example3">Email address</label>
                    <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} id="form3Example3" className="form-control form-control-lg" placeholder="Enter a valid email address" />
                  </div>
 
             
                  <div className="form-outline mb-3">
                    <label className="form-label" for="form3Example4">Password</label>
                    <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} id="form3Example4" className="form-control form-control-lg" placeholder="Enter password" />
                  </div>
 
                  <div className="d-flex justify-content-between align-items-center">
                    <div className="form-check mb-0">
                      <input className="form-check-input me-2" type="checkbox" value="" id="form2Example3" />
                      <label className="form-check-label" for="form2Example3">
                        Remember me
                      </label>
                    </div>
                  </div>
 
                  <div className="text-center text-lg-start mt-4 pt-2">
                  <button type="button" className="btn btn-primary btn-lg" onClick={() => registerUser()} style={{ backgroundColor: 'orange', border: 'none' }}>Sign Up</button>
                    <p className="small mt-2 pt-1 mb-0">Login to your account <a href="/" className="link-primary text-decoration-none">Click here!</a></p>
                  </div>
 
                </form>
              </div>
              <div className="col-md-9 col-lg-6 col-xl-5">
                <img src={imgs[0]} className="img-fluid"/>
              </div>
            </div>
          </div>
        </div>
    </div>
  );
}