(function () {

    function createInspector(containerId, config = {}) {

        const container = document.getElementById(containerId);

        if (!container) {
            console.error("SwarmDigiz container not found");
            return;
        }

        const iframe = document.createElement("iframe");

        const baseUrl = config.baseUrl || "http://localhost:8501";

        const business = config.business || "default";

        iframe.src = `${baseUrl}?embed=true&business=${business}`;

        iframe.style.width = "100%";
        iframe.style.height = "720px";
        iframe.style.border = "none";
        iframe.style.borderRadius = "10px";

        container.appendChild(iframe);
    }

    window.SwarmDigiz = {
        init: createInspector
    };

})();