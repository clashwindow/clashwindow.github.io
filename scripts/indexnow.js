
const fetch = require("node-fetch");

const INDEXNOW_CONFIG = {
  host: "clashwindow.github.io",
  key: "8575fe8139f14b2da85e40bbc8b86ce2",
  urlList: [] // This will be populated dynamically
};

async function submitUrlToIndexNow(url) {
  INDEXNOW_CONFIG.urlList = [url];
  const requestBody = {
    host: INDEXNOW_CONFIG.host,
    key: INDEXNOW_CONFIG.key,
    keyLocation: `https://${INDEXNOW_CONFIG.host}/${INDEXNOW_CONFIG.key}.txt`,
    urlList: INDEXNOW_CONFIG.urlList,
  };

  try {
    const response = await fetch("https://api.indexnow.org/indexnow", {
      method: "POST",
      headers: {
        "Content-Type": "application/json; charset=utf-8",
      },
      body: JSON.stringify(requestBody),
    });

    if (response.ok) {
      console.log(`Successfully submitted ${url} to IndexNow.`);
    } else {
      console.error(`Failed to submit ${url} to IndexNow: ${response.status} - ${response.statusText}`);
      const responseBody = await response.text();
      console.error(`Response body: ${responseBody}`);
    }
  } catch (error) {
    console.error(`Error submitting ${url} to IndexNow: ${error.message}`);
  }
}

// Example usage (this script would typically be called with the new post URL)
// To run this script, you would typically use a command like:
// node scripts/indexnow.js <post_url>
// For example:
// node scripts/indexnow.js https://clashwindow.github.io/category/my-new-post/

// If running directly for testing:
// const testUrl = "https://clashwindow.github.io/category/test-post/";
// submitUrlToIndexNow(testUrl);

module.exports = { submitUrlToIndexNow };
