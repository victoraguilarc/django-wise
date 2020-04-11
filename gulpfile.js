'use strict';

var gulp = require('gulp'),
    watch = require('gulp-watch'),
    browserSync = require("browser-sync"),
    rigger = require('gulp-rigger'),
    reload = browserSync.reload,
    rimraf = require('gulp-rimraf'),
    cleanCSS = require('gulp-clean-css'),
    sass = require('gulp-sass');

var path = {
    bower: {
        jquery: [
            './bower_components/jquery/dist/jquery.min.js',
            './dev/js/vendor/jquery/jquery.min.js']
    },
    dist: { // compiled files
        css: './web/static/assets/css/',
    },
    src: { // development files
        scss: [
            './web/static/assets/scss/transactions.scss',
            './web/static/assets/scss/errors.scss',
            './web/static/assets/scss/home.scss',
        ]
    },
    watch: { // watching files
        js: './web/static/assets/js/**/*.js',
        css: './web/static/assets/scss/**/*.scss',
        fonts: './web/static/assets/css/fonts/**/*.*',
        img: './web/static/assets/img/**/*.*',
        assets: './web/static/assets/assets/*.*'
    },
    clean: './build'
};

var forceReload = {stream: true};
gulp.task('style:build', function () {
    return gulp.src(path.src.scss)
        .pipe(sass())
        // .pipe(cleanCSS())
        .pipe(gulp.dest(path.dist.css))
        .pipe(reload(forceReload));
});


// gulp.task('js:build', function () {
//     gulp.src(path.src.js)
//         .pipe(gulp.dest(path.dist.js));
//
//     return gulp.src(path.src.js)
//         .pipe(gulp.dest(path.dist.js))
//         .pipe(reload(forceReload));
// });



gulp.task('build', [    
    'style:build',
    // 'js:build',
]);

gulp.task('watch', function(){
    watch([path.watch.css], function(event, cb) {
        gulp.start('style:build');
    });

    // watch([path.watch.js], function(event, cb) {
    //     gulp.start('js:build');
    // });

});

gulp.task('clean', function (cb) {
    rimraf(path.clean, cb);    
});

gulp.task('default', ['build', 'watch']);