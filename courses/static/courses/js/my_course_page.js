document.addEventListener('DOMContentLoaded', function() {
    const radioButtons = document.querySelectorAll('.btn-check');

    radioButtons.forEach(button => {
        button.addEventListener('change', function() {
            const status = this.value;
            filterCoursesByStatus(status);
        });
    });

    function filterCoursesByStatus(status) {
        const courses = document.querySelectorAll('.col[data-status]');

        courses.forEach(course => {
            const courseStatus = course.getAttribute('data-status');
            if (status === 'all' || courseStatus === status) {
                course.style.display = 'block';
            } else {
                course.style.display = 'none';
            }
        });
    }
});