document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('will-form');
    const willOutput = document.getElementById('will-output');
    const poaOutput = document.getElementById('poa-output');
    const navLinks = document.querySelectorAll('#form-nav a');

    form.addEventListener('submit', function(event) {
        event.preventDefault();

        // Get form values
        const fullName = document.getElementById('fullName').value;
        const address = document.getElementById('address').value;
        const executorName = document.getElementById('executorName').value;
        const executorAddress = document.getElementById('executorAddress').value;
        const guardianName = document.getElementById('guardianName').value;
        const beneficiaries = document.getElementById('beneficiaries').value;
        const attorneyName = document.getElementById('attorneyName').value;
        const attorneyAddress = document.getElementById('attorneyAddress').value;
        const effectiveDate = document.getElementById('effectiveDate').value;

        // Generate Will Text
        const willText = `
LAST WILL AND TESTAMENT
OF
${fullName.toUpperCase()}

I, ${fullName}, residing at ${address}, being of sound mind and memory, do hereby declare this to be my Last Will and Testament.

1. EXECUTOR: I appoint ${executorName}, residing at ${executorAddress}, as the Executor of my will.

2. GUARDIAN: In the event of my death, if I have any minor children, I appoint ${guardianName || '________________'} as their guardian.

3. BENEFICIARIES: I give all my property to the following individuals: ${beneficiaries}.

Signed on this day: ${new Date().toLocaleDateString()}
_________________________
(Signature)
        `;

        // Generate POA Text
        const poaText = `
POWER OF ATTORNEY

I, ${fullName}, residing at ${address}, hereby appoint ${attorneyName}, residing at ${attorneyAddress}, as my attorney-in-fact.

This Power of Attorney shall become effective on ${effectiveDate}.

My attorney-in-fact shall have the full power and authority to act on my behalf.

Date: ${new Date().toLocaleDateString()}
_________________________
(Signature)
        `;

        // Display the generated documents
        willOutput.textContent = willText;
        poaOutput.textContent = poaText;
        document.getElementById('output').style.display = 'block';
    });
    
    // Smooth scrolling for navigation links
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            if(targetElement) {
                targetElement.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
});