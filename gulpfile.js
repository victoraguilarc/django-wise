let gulp = require('gulp');
let sass = require('gulp-sass');
let sourcemaps = require('gulp-sourcemaps');
let changed = require('gulp-changed');
let grep = require('gulp-grep');
let minifyCss= require('gulp-minify-css');
let uglifyJs = require('gulp-uglify');
let concat = require('gulp-concat');

sass.compiler = require('node-sass');


let paths = {
  dist: 'web/static/dist',
  images: 'web/static/**/*.{JPG,jpg,png,gif}',
  sass: 'web/static/assets/**/*.scss',
  scripts: 'web/static/assets/**/*.js',
};

gulp.task('sass:prod', () => {
  return gulp.src(paths.sass)
    .pipe(sourcemaps.init())
    .pipe(sass())
    .pipe(changed(paths.dist))
    .pipe(sourcemaps.write('.', { sourceRoot: '/' }))
    .pipe(grep('**/*.css', { read: false, dot: true }))
    .pipe(minifyCss({ keepSpecialComments: 0 }))
    .pipe(gulp.dest(paths.dist))
});

gulp.task('scripts:prod', () => {
  return gulp.src(paths.scripts)
    .pipe(uglifyJs())
    .pipe(changed(paths.dist))
    .pipe(gulp.dest(paths.dist))
});

gulp.task('default', gulp.series(['sass:prod', 'scripts:prod']));
