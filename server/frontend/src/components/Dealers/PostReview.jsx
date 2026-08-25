import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import "./Dealers.css";
import "../assets/style.css";
import Header from "../Header/Header";

const PostReview = () => {
  const [dealer, setDealer] = useState({});
  const [review, setReview] = useState("");
  const [model, setModel] = useState("");
  const [year, setYear] = useState("");
  const [date, setDate] = useState("");
  const [carmodels, setCarmodels] = useState([]);

  const params = useParams();
  const id = params.id;

  let curr_url = window.location.href;
  let root_url = curr_url.substring(0, curr_url.indexOf("postreview"));

  const dealer_url = root_url + `djangoapp/dealer/${id}`;
  const review_url = root_url + "djangoapp/add_review";
  const carmodels_url = root_url + "djangoapp/get_cars";

  const postreview = async () => {
    let firstname = sessionStorage.getItem("firstname");
    let lastname = sessionStorage.getItem("lastname");
    let username = sessionStorage.getItem("username");

    let name = `${firstname} ${lastname}`;

    // Use username if first/last name are unavailable
    if (
      !firstname ||
      !lastname ||
      firstname === "null" ||
      lastname === "null"
    ) {
      name = username;
    }

    // Validate form
    if (!model || !review || !date || !year) {
      alert("All details are mandatory");
      return;
    }

    /*
     * Instead of split(" "), use the selected CarModel object.
     * Some makes/models contain spaces, so split(" ") can produce
     * incorrect values.
     */
    const selectedCar = carmodels.find(
      (car) => `${car.CarMake} ${car.CarModel}` === model
    );

    if (!selectedCar) {
      alert("Please select a valid car make and model.");
      return;
    }

    const jsoninput = {
      name: name,
      dealership: parseInt(id),
      review: review,
      purchase: true,
      purchase_date: date,
      car_make: selectedCar.CarMake,
      car_model: selectedCar.CarModel,
      car_year: parseInt(year),
    };

    console.log("Submitting review:", jsoninput);
    console.log("POST URL:", review_url);

    try {
      const res = await fetch(review_url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(jsoninput),
      });

      console.log("HTTP status:", res.status);

      const json = await res.json();

      console.log("Server response:", json);

      if (json.status === 200) {
        // Go back to dealer details
        window.location.href = root_url + `dealer/${id}`;
      } else {
        console.error("Review submission failed:", json);
        alert(
          "Review could not be submitted. Check the browser console for details."
        );
      }
    } catch (error) {
      console.error("Error posting review:", error);
      alert("Error submitting review. Check the browser console.");
    }
  };

  const get_dealer = async () => {
    try {
      const res = await fetch(dealer_url, {
        method: "GET",
      });

      const retobj = await res.json();

      if (retobj.status === 200) {
        /*
         * Your dealer API response contains a dealer object.
         * Support both an object and an array to avoid crashing.
         */
        if (Array.isArray(retobj.dealer)) {
          if (retobj.dealer.length > 0) {
            setDealer(retobj.dealer[0]);
          }
        } else {
          setDealer(retobj.dealer);
        }
      }
    } catch (error) {
      console.error("Error getting dealer:", error);
    }
  };

  const get_cars = async () => {
    try {
      const res = await fetch(carmodels_url, {
        method: "GET",
      });

      const retobj = await res.json();

      console.log("Car models:", retobj);

      if (retobj.CarModels) {
        setCarmodels(Array.from(retobj.CarModels));
      }
    } catch (error) {
      console.error("Error getting cars:", error);
    }
  };

  useEffect(() => {
    get_dealer();
    get_cars();

    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div>
      <Header />

      <div style={{ margin: "5%" }}>
        <h1 style={{ color: "darkblue" }}>
          {dealer.full_name}
        </h1>

        <textarea
          id="review"
          cols="50"
          rows="7"
          value={review}
          placeholder="Enter your review"
          onChange={(e) => setReview(e.target.value)}
        />

        <div className="input_field">
          Purchase Date
          <input
            type="date"
            value={date}
            onChange={(e) => setDate(e.target.value)}
          />
        </div>

        <div className="input_field">
          Car Make

          <select
            name="cars"
            id="cars"
            value={model}
            onChange={(e) => setModel(e.target.value)}
          >
            <option value="" disabled>
              Choose Car Make and Model
            </option>

            {carmodels.map((carmodel, index) => (
              <option
                key={index}
                value={`${carmodel.CarMake} ${carmodel.CarModel}`}
              >
                {carmodel.CarMake} {carmodel.CarModel}
              </option>
            ))}
          </select>
        </div>

        <div className="input_field">
          Car Year
          <input
            type="number"
            value={year}
            onChange={(e) => setYear(e.target.value)}
            min="2015"
            max="2026"
          />
        </div>

        <div>
          <button
            className="postreview"
            type="button"
            onClick={postreview}
          >
            Post Review
          </button>
        </div>
      </div>
    </div>
  );
};

export default PostReview;