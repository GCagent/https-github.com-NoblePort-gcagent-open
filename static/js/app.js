// Dual-Platform Video Uploader - Client-side JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const showComparisonBtn = document.getElementById('showComparison');
    const comparisonPanel = document.getElementById('comparisonPanel');
    const uploadForm = document.getElementById('uploadForm');
    const platformCheckboxes = document.querySelectorAll('input[name="platform"]');
    const youtubeOptions = document.getElementById('youtubeOptions');
    const uploadProgress = document.getElementById('uploadProgress');
    const uploadResults = document.getElementById('uploadResults');
    const submitBtn = document.getElementById('submitBtn');

    // Toggle comparison panel
    showComparisonBtn.addEventListener('click', function() {
        if (comparisonPanel.style.display === 'none') {
            comparisonPanel.style.display = 'block';
            showComparisonBtn.textContent = 'Hide Detailed Comparison';
        } else {
            comparisonPanel.style.display = 'none';
            showComparisonBtn.textContent = 'Show Detailed Comparison';
        }
    });

    // Show/hide YouTube options based on platform selection
    function updateYoutubeOptions() {
        const youtubeChecked = Array.from(platformCheckboxes).some(
            cb => cb.value === 'youtube' && cb.checked
        );
        youtubeOptions.style.display = youtubeChecked ? 'block' : 'none';
    }

    platformCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', updateYoutubeOptions);
    });

    // Form submission
    uploadForm.addEventListener('submit', async function(e) {
        e.preventDefault();

        // Validate platform selection
        const selectedPlatforms = Array.from(platformCheckboxes)
            .filter(cb => cb.checked)
            .map(cb => cb.value);

        if (selectedPlatforms.length === 0) {
            alert('Please select at least one platform');
            return;
        }

        // Get form data
        const formData = new FormData();
        formData.append('video', document.getElementById('videoFile').files[0]);
        formData.append('title', document.getElementById('title').value);
        formData.append('description', document.getElementById('description').value);
        formData.append('tags', document.getElementById('tags').value);
        formData.append('platforms', JSON.stringify(selectedPlatforms));
        formData.append('privacy', document.getElementById('privacy').value);
        formData.append('category', document.getElementById('category').value);

        // Show copyright warnings
        const proceed = await showCopyrightWarnings(selectedPlatforms);
        if (!proceed) {
            return;
        }

        // Show progress
        uploadProgress.style.display = 'block';
        uploadResults.style.display = 'none';
        submitBtn.disabled = true;
        submitBtn.textContent = 'Uploading...';

        // Simulate progress (real progress would need WebSocket or polling)
        let progress = 0;
        const progressInterval = setInterval(() => {
            progress += 2;
            if (progress <= 90) {
                document.getElementById('progressFill').style.width = progress + '%';
                document.getElementById('progressText').textContent = `Uploading... ${progress}%`;
            }
        }, 500);

        try {
            const response = await fetch('/api/upload', {
                method: 'POST',
                body: formData
            });

            clearInterval(progressInterval);

            const result = await response.json();

            // Complete progress
            document.getElementById('progressFill').style.width = '100%';
            document.getElementById('progressText').textContent = 'Upload complete!';

            // Show results
            setTimeout(() => {
                displayResults(result);
                uploadProgress.style.display = 'none';
                submitBtn.disabled = false;
                submitBtn.textContent = 'Upload Video';
                uploadForm.reset();
            }, 1000);

        } catch (error) {
            clearInterval(progressInterval);
            uploadProgress.style.display = 'none';
            submitBtn.disabled = false;
            submitBtn.textContent = 'Upload Video';

            uploadResults.innerHTML = `
                <div class="result-card error">
                    <h3>❌ Upload Failed</h3>
                    <p>Error: ${error.message}</p>
                </div>
            `;
            uploadResults.style.display = 'block';
        }
    });

    // Show copyright warnings dialog
    async function showCopyrightWarnings(platforms) {
        let message = 'COPYRIGHT POLICY WARNING\n\n';

        if (platforms.includes('youtube')) {
            message += 'YOUTUBE (HIGH RISK):\n';
            message += '- Automated Content ID scanning\n';
            message += '- Immediate blocking possible\n';
            message += '- Channel strikes for violations\n';
            message += '- Monetization may be blocked\n\n';
        }

        if (platforms.includes('dtube')) {
            message += 'DTUBE (LOW RISK):\n';
            message += '- No automated scanning\n';
            message += '- You remain legally liable\n';
            message += '- DMCA claims still possible\n';
            message += '- Content persists on IPFS\n\n';
        }

        message += 'Do you want to proceed with the upload?';

        return confirm(message);
    }

    // Display upload results
    function displayResults(result) {
        uploadResults.innerHTML = '';

        if (result.success && result.results) {
            result.results.forEach(platformResult => {
                if (platformResult.success) {
                    const card = createSuccessCard(platformResult);
                    uploadResults.appendChild(card);
                } else {
                    const card = createErrorCard(platformResult);
                    uploadResults.appendChild(card);
                }
            });
        } else {
            const errorCard = document.createElement('div');
            errorCard.className = 'result-card error';
            errorCard.innerHTML = `
                <h3>❌ Upload Failed</h3>
                <p>${result.error || 'Unknown error occurred'}</p>
            `;
            uploadResults.appendChild(errorCard);
        }

        uploadResults.style.display = 'block';
    }

    // Create success result card
    function createSuccessCard(result) {
        const card = document.createElement('div');
        card.className = 'result-card success';

        const platform = result.platform.toUpperCase();
        const icon = result.platform === 'youtube' ? '📺' : '🌐';

        let content = `
            <h3>${icon} ${platform} Upload Successful!</h3>
            <p><strong>URL:</strong> <a href="${result.url}" target="_blank">${result.url}</a></p>
        `;

        if (result.video_id) {
            content += `<p><strong>Video ID:</strong> ${result.video_id}</p>`;
        }

        if (result.ipfs_hash) {
            content += `<p><strong>IPFS Hash:</strong> ${result.ipfs_hash}</p>`;
            content += `<p><strong>IPFS Gateway:</strong> <a href="${result.ipfs_gateway}" target="_blank">${result.ipfs_gateway}</a></p>`;
        }

        if (result.note) {
            content += `<p><em>${result.note}</em></p>`;
        }

        card.innerHTML = content;
        return card;
    }

    // Create error result card
    function createErrorCard(result) {
        const card = document.createElement('div');
        card.className = 'result-card error';

        const platform = result.platform.toUpperCase();

        card.innerHTML = `
            <h3>❌ ${platform} Upload Failed</h3>
            <p>${result.error}</p>
        `;

        return card;
    }

    // Load copyright policies on page load
    loadCopyrightPolicies();

    async function loadCopyrightPolicies() {
        try {
            const response = await fetch('/api/copyright-policies');
            const data = await response.json();
            console.log('Copyright policies loaded:', data);
        } catch (error) {
            console.error('Failed to load copyright policies:', error);
        }
    }
});
