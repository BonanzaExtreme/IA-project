let currentstep = 1;

const userData = {
  level: "",
  age: "",
  goal: "",
  equipment: "",
  body_part: "",
};

window.onload = () => {
  document.getElementById(`step-${currentstep}`).style.display = "block";
  updateProgressbar();
  enableNextButton();

  const likedExercises =
    JSON.parse(localStorage.getItem("likedExercises")) || [];
  likedExercises.forEach((exerciseId) => {
    updateLikeButton(exerciseId);
  });
};

function enableNextButton() {
  const currentStepButtons = document.querySelectorAll(
    `#step-${currentstep} .big-button`
  );
  const nextButton = document.getElementById(`next-${currentstep}`);

  const anySelected = Array.from(currentStepButtons).some((btn) =>
    btn.classList.contains("selected")
  );

  nextButton.disabled = !anySelected;
}
function nextStep(step) {
  if (step < 5 && isStepValid(step)) {
    document.getElementById(`step-${step}`).style.display = "none";
    currentstep++;
    document.getElementById(`step-${currentstep}`).style.display = "block";
    updateProgressbar();
    enableNextButton();
  }
}

function previousStep(step) {
  if (step > 1) {
    document.getElementById(`step-${step}`).style.display = "none";
    currentstep--;
    document.getElementById(`step-${currentstep}`).style.display = "block";
    updateProgressbar();
    enableNextButton();
  }
}

function isStepValid(step) {
  return userData[step] !== "";
}

function updateProgressbar() {
  const circles = document.querySelectorAll(".circle");
  const indicator = document.querySelector(".indicator");

  circles.forEach((circle, index) => {
    if (index < currentstep) {
      circle.classList.add("active");
    } else {
      circle.classList.remove("active");
    }
  });

  const progressPercentage = (currentstep / circles.length) * 100;
  indicator.style.width = progressPercentage + "%";
}

function selectOption(type, value) {
  userData[type] = value;
  console.log(userData);
  const currentStepButtons = document.querySelectorAll(
    `#step-${currentstep} .big-button`
  );

  currentStepButtons.forEach((button) => {
    button.classList.remove("selected");
  });

  const selectedbutton = Array.from(currentStepButtons).find(
    (button) => button.innerText.toLowerCase() == value.toLowerCase()
  );

  if (selectedbutton) {
    selectedbutton.classList.add("selected");
  }

  enableNextButton();
}

function generateRecommendations(event) {
  event.preventDefault();
  console.log("Sending user data:", userData);
  fetch("/generate_workout", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(userData),
  })
    .then((response) => response.json())
    .then((recommendations) => {
      const recommendationList = document.getElementById("exercise-list-2");
      recommendationList.innerHTML = "";

      recommendations.forEach((exercise) => {
        const exerciseContainer = document.createElement("div");
        exerciseContainer.classList.add("exercise-container-2");

        const nameElement = document.createElement("h3");
        nameElement.classList.add("exercise-name");
        nameElement.textContent = exercise.name;

        const descriptionElement = document.createElement("p");
        descriptionElement.classList.add("exercise-description");
        descriptionElement.textContent = `Description: ${exercise.description}`;

        const typeElement = document.createElement("p");
        typeElement.classList.add("exercise-type");
        typeElement.textContent = `Type: ${exercise.type}`;

        const equipmentElement = document.createElement("p");
        equipmentElement.classList.add("exercise-equipment");
        equipmentElement.textContent = `Equipment: ${exercise.equipment}`;

        const targetElement = document.createElement("p");
        targetElement.classList.add("exercise-target");
        targetElement.textContent = `Target: ${exercise.target}`;

        const instructionsElement = document.createElement("p");
        instructionsElement.classList.add("exercise-instructions");
        instructionsElement.textContent = `Instructions: ${exercise.instructions}`;

        const repsElement = document.createElement("p");
        repsElement.classList.add("exercise-reps");
        repsElement.textContent = `Reps: ${exercise.reps}`;

        const instructionsButton = document.createElement("button");
        instructionsButton.classList.add("instructions-button");
        instructionsButton.textContent = "Show Instructions";

        instructionsButton.addEventListener("click", () => {
          instructionsElement.classList.toggle("visible");
          if (instructionsElement.classList.contains("visible")) {
            instructionsButton.textContent = "Hide Instructions";
          } else {
            instructionsButton.textContent = "Show Instructions";
          }
        });

        exerciseContainer.appendChild(nameElement);
        exerciseContainer.appendChild(descriptionElement);
        exerciseContainer.appendChild(typeElement);
        exerciseContainer.appendChild(equipmentElement);
        exerciseContainer.appendChild(targetElement);
        exerciseContainer.appendChild(instructionsElement);
        exerciseContainer.appendChild(instructionsButton);
        exerciseContainer.appendChild(repsElement);

        const recommendationList = document.getElementById("exercise-list-2");
        recommendationList.appendChild(exerciseContainer);
      });

      document.getElementById("recommendations-container").style.display =
        "block";
    })
    .catch((error) => {
      console.error("Error generating workout recommendations:", error);
    });
}

document
  .getElementById("assessment-form")
  .addEventListener("submit", function (event) {
    event.preventDefault;
    console.log("User data before submission", userData);
    generateRecommendations(event);
  });

function toggleLike(exerciseId) {
  let likedExercises = JSON.parse(localStorage.getItem("likedExercises")) || [];

  const index = likedExercises.indexOf(exerciseId);

  if (index > -1) {
    likedExercises.splice(index, 1);
  } else {
    likedExercises.push(exerciseId);
  }

  localStorage.setItem("likedExercises", JSON.stringify(likedExercises));

  updateLikeButton(exerciseId);
}

function updateLikeButton(exerciseId) {
  const likedExercises =
    JSON.parse(localStorage.getItem("likedExercises")) || [];
  const likeButton = document.getElementById(`like-btn-${exerciseId}`);
  const heartIcon = likeButton.querySelector("i");

  if (likedExercises.includes(exerciseId)) {
    likeButton.textContent = "Unlike";
    likeButton.appendChild(heartIcon);
    likeButton.classList.add("liked");
  } else {
    likeButton.textContent = "Like";
    likeButton.appendChild(heartIcon);
    likeButton.classList.remove("liked");
  }
}
