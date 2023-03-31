
document.addEventListener("DOMContentLoaded", function () {
    toggleMETParametersSelection();
});

function toggleMETParametersSelection() {
    let demo = document.getElementById('demo');
    let metToCalorieParameters = document.getElementById('metToCalorieParameters');

    // Some demos need these additional parameters:  weight, height, age, gender
    // NOTE: New demos requiring these should be added to the list below.
    let demosWithMETParameters = ["run_calorie_estimation", "run_fitness_tracker"];

    if (demosWithMETParameters.includes(demo.value)) {
        metToCalorieParameters.classList.remove('uk-hidden');
    } else {
        metToCalorieParameters.classList.add('uk-hidden');
    }
}

async function getSupportedModelsByDemo(url) {
    let demo = document.getElementById('demo');
    let modelName = document.getElementById('modelName');
    data = {
        'demo': demo.value
    };

    let response = await asyncRequest(url, data);
    modelName.innerHTML = null;
    let models = response['models'];

    if (models.length > 0) {
        modelName.classList.remove('uk-form-danger');
        for (model of models) {
            modelName.insertAdjacentHTML('beforeend', `<option>${model}</option>`);
        }
    } else {
        modelName.classList.add('uk-form-danger');
        modelName.insertAdjacentHTML('beforeend', `<option value="">No models available</option>`);
    }

}

function addMessageToDemoTerminal(message) {
    let terminal = document.getElementById('demoTerminal');
    terminal.insertAdjacentHTML('beforeend', `<div class='monospace-font'><b>${message}</b></div>`);
    terminal.scrollTop = terminal.scrollHeight;
}

function streamDemo(message) {
    let frame = document.getElementById('frame');
    frame.src = message.image;
    frame.width = message.width;
    frame.height = message.height;
}

async function startDemo(url) {
    let demo = document.getElementById('demo');
    let modelName = document.getElementById('modelName').value;

    let weight = document.getElementById('weight').value;
    let age = document.getElementById('age').value;
    let height = document.getElementById('height').value;
    let gender = document.getElementById('gender').value;
    let title = document.getElementById('title').value;
    let gpuInput = document.getElementById('gpuInput').checked;

    let webcamInput = document.getElementsByName('inputSource')[0];
    let inputVideoPath = document.getElementById('inputVideoPath');
    let inputVideoPathValue = (webcamInput.checked) ? '' : inputVideoPath.value;

    let saveVideo = document.getElementById('saveVideo');
    let outputVideoName = document.getElementById('outputVideoName');
    let outputVideoNameValue = (saveVideo.checked) ? outputVideoName.value : '';

    let buttonRunDemo = document.getElementById('buttonRunDemo');
    let buttonCancelDemo = document.getElementById('buttonCancelDemo');

    let frame = document.getElementById('frame');
    let terminal = document.getElementById('demoTerminal');
    terminal.innerHTML = '';

    data = {
        demo: demo.options[demo.selectedIndex].text,
        modelName: modelName,
        inputVideoPath: inputVideoPathValue,
        outputVideoName: outputVideoNameValue,
        height: height,
        weight: weight,
        age: age,
        gender: gender,
        title: title,
        gpuInput: gpuInput,
    };

    buttonRunDemo.disabled = true;
    buttonCancelDemo.disabled = false;

    await asyncRequest(url, data);

    let socket = io.connect('/stream-demo');
    socket.on('connect', function() {
        console.log('Socket Connected');
        socket.emit('stream_demo', {status: 'Socket Connected'});
    });

    socket.on('stream_frame', function(message) {
        streamDemo(message);
    });

    socket.on('success', function(message) {
        if (message.status === 'Complete') {
            addMessageToDemoTerminal('Stopped Inference...');
            frame.removeAttribute('src');
            // Set frame placeholder to default height and width
            frame.height = 480;
            frame.width = 640;
            socket.disconnect();
            console.log('Socket Disconnected');

            buttonCancelDemo.disabled = true;

            // Enable run demo button again depending on input fields
            checkInputFields();
        }
    });

    socket.on('demo_logs', function(message) {
        addMessageToDemoTerminal(message.log);
    });

    addMessageToDemoTerminal('Starting Inference...');
}

async function cancelDemo(url) {
    await asyncRequest(url);

    document.getElementById('buttonCancelDemo').disabled = true;

    // Enable run demo button again depending on input fields
    checkInputFields();
}

function toggleInputVideoField() {
    let webcamInput = document.getElementsByName('inputSource')[0];
    let inputVideoDiv = document.getElementById('inputVideoDiv');

    if (webcamInput.checked) {
        inputVideoDiv.classList.add('uk-hidden');
    } else {
        inputVideoDiv.classList.remove('uk-hidden');
    }

    checkInputFields();
}

function toggleOutputVideoField() {
    let saveVideo = document.getElementById('saveVideo');
    let outputVideoDiv = document.getElementById('outputVideoDiv');

    if (saveVideo.checked) {
        outputVideoDiv.classList.remove('uk-hidden');
    } else {
        outputVideoDiv.classList.add('uk-hidden');
    }

    checkInputFields();
}

async function checkInputFields() {
    let webcamInput = document.getElementsByName('inputSource')[0];
    let inputVideoPathLabel = document.getElementById('inputVideoPathLabel');
    let inputVideoPath = document.getElementById('inputVideoPath');
    let inputVideoPathValue = inputVideoPath.value;

    let saveVideo = document.getElementById('saveVideo');
    let outputVideoNameLabel = document.getElementById('outputVideoNameLabel');
    let outputVideoName = document.getElementById('outputVideoName');
    let outputVideoNameValue = outputVideoName.value;

    let buttonRunDemo = document.getElementById('buttonRunDemo');
    let buttonCancelDemo = document.getElementById('buttonCancelDemo');

    let directoriesResponse = await browseDirectory(inputVideoPathValue, '');

    let disabled = false;

    // Check that input video path is filled and exists if not streaming from webcam
    if (webcamInput.checked) {
        setFormWarning(inputVideoPathLabel, inputVideoPath, '');
    } else if (inputVideoPathValue === '') {
        setFormWarning(inputVideoPathLabel, inputVideoPath, 'Please provide an input video');
        disabled = true;
    } else if (!directoriesResponse.path_exists) {
        setFormWarning(inputVideoPathLabel, inputVideoPath, 'This path does not exist');
        disabled = true;
    } else if (!inputVideoPathValue.endsWith('.mp4')) {
        setFormWarning(inputVideoPathLabel, inputVideoPath, 'Please provide a valid .mp4 file');
        disabled = true;
    } else {
        // Correct path provided
        setFormWarning(inputVideoPathLabel, inputVideoPath, '');
    }

    // Check that output video name is provided if video should be saved
    if (!saveVideo.checked) {
        setFormWarning(outputVideoNameLabel, outputVideoName, '');
    } else if (!outputVideoNameValue) {
        setFormWarning(outputVideoNameLabel, outputVideoName, 'Please provide a video name');
        disabled = true;
    } else {
        // Name provided
        setFormWarning(outputVideoNameLabel, outputVideoName, '');
    }

    // Don't enable the run demo button, if the model is currently running (i.e. Cancel button is enabled)
    if (!buttonCancelDemo.disabled) {
        disabled = true;
    }

    buttonRunDemo.disabled = disabled;
}


