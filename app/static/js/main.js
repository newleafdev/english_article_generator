async function generateContent() {
    const content_type = document.querySelector('input[name="content_type"]:checked').value;
    const topic = document.getElementById('topic').value;
    const levels = [...document.querySelectorAll('input[name="levels"]:checked')].map(cb => cb.value);
    const exercise_types = [...document.querySelectorAll('input[name="exercises"]:checked')].map(cb => cb.value);

    if (!topic) {
        alert('Please enter a topic');
        return;
    }

    if (levels.length === 0) {
        alert('Please select at least one level');
        return;
    }

    if (exercise_types.length === 0) {
        alert('Please select at least one exercise type');
        return;
    }

    // Show loading state
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '<div class="loading">Generating content... This may take a few moments...</div>';
    
    // Disable the generate button
    const generateButton = document.querySelector('button');
    generateButton.disabled = true;
    generateButton.textContent = 'Generating...';

    try {
        const response = await fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                content_type,
                topic,
                levels,
                exercise_types
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Failed to generate content');
        }

        const data = await response.json();
        displayResults(data);
    } catch (error) {
        resultsDiv.innerHTML = `<div class="error">Error: ${error.message}</div>`;
    } finally {
        // Re-enable the generate button
        generateButton.disabled = false;
        generateButton.textContent = 'Generate Content';
    }
}

function displayResults(data) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '';

    for (const [level, content] of Object.entries(data)) {
        const section = document.createElement('div');
        section.className = 'section';
        section.innerHTML = `
            <h2>${level} Content</h2>
            <div class="content">${content.content.replace(/\n/g, '<br>')}</div>
            <h3>Exercises</h3>
            ${content.exercises.map(ex => `
                <div class="exercise">
                    <h4>${ex.type}</h4>
                    <div>${ex.content.replace(/\n/g, '<br>')}</div>
                </div>
            `).join('')}
        `;
        resultsDiv.appendChild(section);
    }
}