// Wait for the DOM to be fully loaded before running the script
document.addEventListener("DOMContentLoaded", () => {
    
    // Get the two elements we need
    const guidelinesBox = document.getElementById("guidelines-box");
    const continueBtn = document.getElementById("continue-btn");

    // Add a scroll event listener to the guidelines box
    guidelinesBox.addEventListener("scroll", () => {
        
        // This calculates if the user is at the bottom
        // (scrollHeight) = total height of the content
        // (scrollTop) = how far down the user has scrolled
        // (clientHeight) = the visible height of the box
        
        // We check if (scrolled + visible_height) is at the bottom
        // We add a small 5px buffer to be safe
        if (guidelinesBox.scrollTop + guidelinesBox.clientHeight >= guidelinesBox.scrollHeight - 5) {
            
            // If at the bottom, remove the disabled class
            continueBtn.classList.remove("button-disabled");
            
            // And add the enabled class
            continueBtn.classList.add("button-enabled");
        }
    });

});