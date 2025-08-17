const API_ENDPOINT = "/predict";

const imageUpload = document.getElementById("imageUpload");
const predictButton = document.getElementById("predictButton");
const resultText = document.getElementById("resultText");
const imagePreview = document.getElementById("imagePreview");
let uploadedFile = null;

imageUpload.addEventListener("change", (event) => {
  // get the selected file
  uploadedFile = event.target.files[0];
  if (uploadedFile) {
    // clear previous preview
    imagePreview.innerHTML = "";
    // create an image element to show a preview
    const reader = new FileReader();
    reader.onload = function (e) {
      const img = document.createElement("img");
      img.src = e.target.result;
      img.style.maxWidth = "300px"; // preview size
      imagePreview.appendChild(img);
    };
    reader.readAsDataURL(uploadedFile);
    resultText.innerText = "...";
  }
});

predictButton.addEventListener("click", async () => {
  if (!uploadedFile) {
    alert("Please select an image first!");
    return;
  }
  resultText.innerText = "Predicting...";
  // create a FormData object to send the file
  const formData = new FormData();
  formData.append("file", uploadedFile);

  try {
    const response = await fetch(API_ENDPOINT, {
      method: "POST",
      body: formData,
    });

    const data = await response.json();
    if (data.error) {
      resultText.innerText = "Error: " + data.error;
    } else {
      resultText.innerText = `Prediction: ${data.prediction} (Confidence: ${(
        data.confidence * 100
      ).toFixed(2)}%)`;
    }
  } catch (err) {
    resultText.innerText = "Prediction failed.";
  }
});
