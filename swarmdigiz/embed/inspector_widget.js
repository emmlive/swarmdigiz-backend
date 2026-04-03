// =====================================================
// CONFIG
// =====================================================

// 🔥 UPDATE THIS WHEN YOU CHANGE ENV (ngrok → production)
const API_URL = "https://wholesomely-unestimable-isadora.ngrok-free.dev/api/inspection";


// =====================================================
// SUBMIT HANDLER
// =====================================================

async function submitInspection(formData) {

    try {

        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "ngrok-skip-browser-warning": "true"
            },
            body: JSON.stringify(formData)
        });

        // ✅ Handle non-200 responses safely
        if (!response.ok) {
            throw new Error(`HTTP error: ${response.status}`);
        }

        const data = await response.json();

        if (!data.success) {
            throw new Error("API returned failure");
        }

        renderResult(data, formData);

    } catch (err) {
        console.error("❌ Inspection error:", err);
        alert("Something went wrong. Please try again.");
    }
}


// =====================================================
// RENDER RESULT
// =====================================================

function renderResult(data, formData) {

    const container = document.getElementById("inspection-result");

    const tierColor = {
        hot: "#ef4444",
        warm: "#f59e0b",
        cold: "#10b981"
    };

    container.innerHTML = `
        <div style="
            background:#020617;
            border:1px solid #1e293b;
            padding:24px;
            border-radius:12px;
            text-align:center;
        ">
            <h2 style="font-size:28px;margin-bottom:10px;">
                Estimated Price: $${(data.quote / 100).toFixed(2)}
            </h2>

            <p style="color:${tierColor[data.lead_tier] || "#fff"}; font-weight:600;">
                Lead Quality: ${(data.lead_tier || "unknown").toUpperCase()}
            </p>

            <p style="color:#94a3b8; margin-top:10px;">
                Based on your home size and condition
            </p>

            <button onclick="startBookingFlow('${formData.phone}', '${data.quote}')"
                style="
                    margin-top:20px;
                    background:#3b82f6;
                    color:#fff;
                    padding:14px 24px;
                    border:none;
                    border-radius:8px;
                    cursor:pointer;
                    font-weight:600;
                ">
                Book This Service →
            </button>
        </div>
    `;
}


// =====================================================
// BOOKING FLOW (LEAD → CONVERSION)
// =====================================================

function startBookingFlow(phone, quote) {

    // 🔥 OPTION 1 — Redirect to booking page
    window.location.href = `/booking?phone=${encodeURIComponent(phone)}&quote=${quote}`;

    // 🔥 OPTION 2 (future): modal / inline booking
}


// =====================================================
// FORM HOOK
// =====================================================

document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("inspection-form");

    if (!form) {
        console.warn("⚠️ inspection-form not found");
        return;
    }

    form.addEventListener("submit", function (e) {

        e.preventDefault();

        const formData = {
            service_type: document.getElementById("service").value,
            home_size: document.getElementById("size").value,
            business_id: "airductify_main",
            condition: document.getElementById("condition").value,
            name: document.getElementById("name").value,
            phone: document.getElementById("phone").value
        };

        submitInspection(formData);
    });

});