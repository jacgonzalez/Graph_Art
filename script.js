const API_ENDPOINT = "http://0.0.0.0:8000/";

const uploadInput = document.getElementById("uploadInput");
const imageUploadedDiv = document.getElementById("imageUploadedDiv");
const imageResultDiv = document.getElementById("imageResultDiv");
const uploadLabel = document.getElementById("uploadLabel");
const ldsDualRing = document.getElementById("ldsDualRing");
const pointsNumberInput = document.getElementById("pointsNumberInput");
const interationsNumberInput = document.getElementById("interationsNumberInput");
const kInput = document.getElementById("kInput");
const descriptionP = document.getElementById("descriptionP");

const checkParams = () => {
    const pointsNumberInputValue = pointsNumberInput.value;
    const interationsNumberInputValue = interationsNumberInput.value;
    const kInputValue = kInput.value;
    if (!pointsNumberInputValue || !interationsNumberInputValue || !kInputValue) {
        alert("Please fill all the fields")
        return false;
    }

    const points = parseInt(pointsNumberInputValue);
    const iterations = parseInt(interationsNumberInputValue);
    const k = parseInt(kInputValue);
    if (isNaN(points) || isNaN(iterations) || isNaN(k)) {
        alert("Please enter only numeric values")
        return false
    }

    if (k < 1 || k > 5) {
        alert("Please enter a value for K within 1 and 5")
        return false
    }
    return true;
}

const sendImageRequest = (body) =>
    new Promise((resolve, reject) => {
        fetch(API_ENDPOINT, {
            method: 'post',
            body,
        }).then((results) => {
            resolve(results)
        }).catch((error) => {
            reject(error)
        })
    })

const onChooseFile = () => {

    if (!checkParams()) {
        uploadInput.value = null;
        return;
    }

    ldsDualRing.style.display = "flex";

    const inputImage = uploadInput.files[0];
    const file_name = inputImage.name;
    uploadLabel.textContent = `Filename: ${file_name}`
    imageUploadedDiv.src = URL.createObjectURL(inputImage);

    const formData = new FormData();
    formData.append('points', pointsNumberInput.value);
    formData.append('iterations', interationsNumberInput.value);
    formData.append('k', kInput.value);
    formData.append('file', inputImage);


    sendImageRequest(formData)
        .then((results) => {
            return results.blob()
        })
        .then((results) => {
            imageResultDiv.src = URL.createObjectURL(results);
            ldsDualRing.style.display = "none";
            descriptionP.innerText = "The image has been processed successfully!"
            uploadInput.value = null;
        })
}

uploadInput.onchange = onChooseFile;