const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add("show");
        }
    });
}, { threshold: 0.1 });

document.querySelectorAll(".animate").forEach(el => observer.observe(el));

window.addEventListener('load', () => {
    const careerAdvice = document.querySelector('.career-advice-section');
    if (careerAdvice) {
        setTimeout(() => {
            careerAdvice.scrollIntoView({ 
                behavior: 'smooth', 
                block: 'center' 
            });
        }, 500);
    }
});

const form = document.querySelector('form');
const submitBtn = document.querySelector('button[type="submit"]');

if (form && submitBtn) {
    form.addEventListener('submit', () => {
        submitBtn.innerHTML = '<div class="spinner" style="width: 20px; height: 20px; border-width: 3px; display: inline-block; margin-right: 8px;"></div>Analyzing...';
        submitBtn.disabled = true;
    });
}

window.addEventListener('load', () => {
    const progressBars = document.querySelectorAll('.progress-fill');
    progressBars.forEach(bar => {
        const width = bar.style.width;
        bar.style.width = '0%';
        setTimeout(() => {
            bar.style.width = width;
        }, 300);
    });
});

const careerAdviceSection = document.querySelector('.career-advice-section');
if (careerAdviceSection) {
    const copyBtn = document.createElement('button');
    copyBtn.innerHTML = '📋 Copy Advice';
    copyBtn.className = 'copy-btn';
    copyBtn.style.cssText = `
        position: absolute;
        top: 20px;
        right: 20px;
        background: rgba(255, 255, 255, 0.2);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.3);
        padding: 8px 16px;
        border-radius: 8px;
        cursor: pointer;
        font-size: 0.9rem;
        transition: all 0.3s ease;
    `;
    
    copyBtn.addEventListener('mouseenter', () => {
        copyBtn.style.background = 'rgba(255, 255, 255, 0.3)';
    });
    
    copyBtn.addEventListener('mouseleave', () => {
        copyBtn.style.background = 'rgba(255, 255, 255, 0.2)';
    });
    
    copyBtn.addEventListener('click', () => {
        const adviceText = document.querySelector('.advice-content').innerText;
        navigator.clipboard.writeText(adviceText).then(() => {
            copyBtn.innerHTML = '✅ Copied!';
            setTimeout(() => {
                copyBtn.innerHTML = '📋 Copy Advice';
            }, 2000);
        });
    });
    
    careerAdviceSection.style.position = 'relative';
    careerAdviceSection.appendChild(copyBtn);
}