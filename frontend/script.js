async function fetchWeather() {
    const city = document.getElementById("city").value.trim();
    const resultDiv = document.getElementById("result");
    resultDiv.innerHTML = "<p>Fetching weather data...</p>";

    if (!city) {
        resultDiv.innerHTML = "<p>Enter your location.</p>";
        return;
    }

    try {
        const response = await fetch(`http://127.0.0.1:8000/weather?city=${city}`);
        const data = await response.json();

        if (data.error) {
            resultDiv.innerHTML = `<p>${data.error}</p>`;
        } else {
            const { weather, category, playlists } = data;
            resultDiv.innerHTML = `
                <h2>Weather in ${city}</h2>
                <p><strong>Condition:</strong> ${weather} (${category})</p>
                <p>Here are some recommended playlists:</p>
                <ul>
                    ${playlists
                        .map(
                            (link, index) =>
                                `<li><a href="${link}" target="_blank">Playlist ${index + 1}</a></li>`
                        )
                        .join("")}
                </ul>
            `;
        }
    } catch (error) {
        resultDiv.innerHTML = `<p>Error fetching weather data. Please try again later.</p>`;
    }
}
