// DTube Easy Connection App - Client JavaScript

let connected = false;
let ipfsConnected = false;

// Check status on load
document.addEventListener('DOMContentLoaded', function() {
    checkStatus();
    checkIPFSDaemon();
});

// Check connection status
async function checkStatus() {
    try {
        const response = await fetch('/api/status');
        const status = await response.json();

        updateStatus(status);
    } catch (error) {
        console.error('Error checking status:', error);
    }
}

// Update status display
function updateStatus(status) {
    const ipfsStatus = document.getElementById('ipfsStatus');
    const accountStatus = document.getElementById('accountStatus');

    // IPFS status
    if (status.ipfs_connected) {
        ipfsStatus.textContent = 'Connected';
        ipfsStatus.classList.add('connected');
        ipfsConnected = true;
    } else {
        ipfsStatus.textContent = 'Disconnected';
        ipfsStatus.classList.remove('connected');
        ipfsConnected = false;
    }

    // Account status
    if (status.account_connected && status.username) {
        accountStatus.textContent = status.username;
        accountStatus.classList.add('connected');
        connected = true;

        // Show upload section
        document.getElementById('connectionSection').style.display = 'none';
        document.getElementById('uploadSection').style.display = 'block';
        document.getElementById('connectedUsername').textContent = status.username;
    } else {
        accountStatus.textContent = 'Not Connected';
        accountStatus.classList.remove('connected');
        connected = false;
    }
}

// Check if IPFS daemon is running
async function checkIPFSDaemon() {
    try {
        const response = await fetch('/api/check-ipfs');
        const data = await response.json();

        const message = document.getElementById('ipfsMessage');

        if (data.running) {
            message.className = 'message info';
            message.textContent = `✓ IPFS daemon detected (Peer ID: ${data.peer_id.substring(0, 20)}...)`;
        } else {
            message.className = 'message error';
            message.textContent = '⚠ ' + data.message;
        }
    } catch (error) {
        console.error('Error checking IPFS:', error);
    }
}

// Connect to IPFS
async function connectIPFS() {
    const host = document.getElementById('ipfsHost').value;
    const port = document.getElementById('ipfsPort').value;
    const button = document.getElementById('ipfsConnectBtn');
    const message = document.getElementById('ipfsMessage');

    button.disabled = true;
    button.textContent = 'Connecting...';

    try {
        const response = await fetch('/api/connect/ipfs', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ host, port })
        });

        const data = await response.json();

        if (data.success) {
            message.className = 'message success';
            message.textContent = `✓ Connected to IPFS! Peer ID: ${data.peer_id.substring(0, 30)}...`;

            ipfsConnected = true;
            document.getElementById('ipfsStatus').textContent = 'Connected';
            document.getElementById('ipfsStatus').classList.add('connected');

            // Enable account connection
            document.getElementById('accountBox').style.opacity = '1';
            document.getElementById('accountBox').style.pointerEvents = 'auto';
        } else {
            message.className = 'message error';
            message.textContent = '✗ Connection failed: ' + data.error;
        }
    } catch (error) {
        message.className = 'message error';
        message.textContent = '✗ Error: ' + error.message;
    } finally {
        button.disabled = false;
        button.textContent = 'Connect IPFS';
    }
}

// Connect DTube account
async function connectAccount() {
    const username = document.getElementById('dtubeUsername').value.trim();
    const privateKey = document.getElementById('dtubePrivateKey').value.trim();
    const button = document.getElementById('accountConnectBtn');
    const message = document.getElementById('accountMessage');

    if (!username) {
        message.className = 'message error';
        message.textContent = 'Please enter your DTube username';
        return;
    }

    if (!ipfsConnected) {
        message.className = 'message error';
        message.textContent = 'Please connect to IPFS first';
        return;
    }

    button.disabled = true;
    button.textContent = 'Connecting...';

    try {
        const response = await fetch('/api/connect/account', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, private_key: privateKey })
        });

        const data = await response.json();

        if (data.success) {
            message.className = 'message success';
            message.textContent = `✓ Connected as ${data.username}!`;

            setTimeout(() => {
                checkStatus();
            }, 1000);
        } else {
            message.className = 'message error';
            message.textContent = '✗ Connection failed: ' + data.error;
        }
    } catch (error) {
        message.className = 'message error';
        message.textContent = '✗ Error: ' + error.message;
    } finally {
        button.disabled = false;
        button.textContent = 'Connect Account';
    }
}

// Disconnect
async function disconnect() {
    if (!confirm('Disconnect from DTube?')) {
        return;
    }

    try {
        await fetch('/api/disconnect', { method: 'POST' });

        // Reload page to reset state
        window.location.reload();
    } catch (error) {
        alert('Error disconnecting: ' + error.message);
    }
}

// Upload form handling
document.getElementById('uploadForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const fileInput = document.getElementById('videoFile');
    const title = document.getElementById('title').value;
    const description = document.getElementById('description').value;
    const tags = document.getElementById('tags').value;

    if (!fileInput.files[0]) {
        alert('Please select a video file');
        return;
    }

    // Show progress
    document.getElementById('uploadProgress').style.display = 'block';
    document.getElementById('uploadResult').style.display = 'none';
    document.getElementById('progressFill').style.width = '0%';
    document.getElementById('progressText').textContent = 'Preparing upload...';

    // Create form data
    const formData = new FormData();
    formData.append('video', fileInput.files[0]);
    formData.append('title', title);
    formData.append('description', description);
    formData.append('tags', tags);

    // Simulate progress
    let progress = 0;
    const progressInterval = setInterval(() => {
        progress += 2;
        if (progress <= 90) {
            document.getElementById('progressFill').style.width = progress + '%';
            document.getElementById('progressText').textContent = `Uploading to IPFS... ${progress}%`;
        }
    }, 500);

    try {
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });

        clearInterval(progressInterval);
        document.getElementById('progressFill').style.width = '100%';
        document.getElementById('progressText').textContent = 'Processing...';

        const result = await response.json();

        setTimeout(() => {
            document.getElementById('uploadProgress').style.display = 'none';
            displayResult(result);
        }, 1000);

    } catch (error) {
        clearInterval(progressInterval);
        document.getElementById('uploadProgress').style.display = 'none';

        displayResult({
            success: false,
            error: error.message
        });
    }
});

// Display upload result
function displayResult(result) {
    const resultDiv = document.getElementById('uploadResult');
    resultDiv.style.display = 'block';

    if (result.success) {
        resultDiv.className = 'upload-result success';
        resultDiv.innerHTML = `
            <h3>✅ Upload Successful!</h3>
            <p><strong>DTube URL:</strong> <a href="${result.url}" target="_blank">${result.url}</a></p>
            <p><strong>IPFS Hash:</strong> <code>${result.ipfs_hash}</code></p>
            <p><strong>IPFS Gateway:</strong> <a href="${result.gateway_url}" target="_blank">${result.gateway_url}</a></p>
            <p><strong>Permlink:</strong> ${result.permlink}</p>
            <br>
            <p><em>Note: Your video is now stored on IPFS and published to DTube!</em></p>
        `;

        // Reset form
        document.getElementById('uploadForm').reset();
    } else {
        resultDiv.className = 'upload-result error';
        resultDiv.innerHTML = `
            <h3>❌ Upload Failed</h3>
            <p><strong>Error:</strong> ${result.error}</p>
            <p>Please try again or check the console for details.</p>
        `;
    }

    // Scroll to result
    resultDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}
