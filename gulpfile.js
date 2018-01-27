var $ = require('gulp-load-plugins')();
var gulp = require('gulp');
var runSequence = require('run-sequence');

// postcss
var autoprefixer = require('autoprefixer');
var discardempty = require('postcss-discard-empty');
var discardcomments = require('postcss-discard-comments');

var config = {
    publicDir: 'example/static',
    scssDir: 'example/scss',
    autoprefixer: {
        browsers: [
            'Chrome >= 35',
            'Firefox >= 38',
            'Edge >= 12',
            'Explorer >= 10',
            'iOS >= 8',
            'Safari >= 8',
            'Android 2.3',
            'Android >= 4',
            'Opera >= 12'
        ],
        "cascade": false
    },
    sass: {
        "includePaths": [
            'node_modules'
        ]
    },
    cssmin: {}
};


/*
 * Karma CSS
 */
gulp.task('scss', function () {
    return gulp.src(config.scssDir + '/*.scss')
        .pipe($.sourcemaps.init())
        .pipe($.sass(config.sass))
        .pipe($.postcss([
            discardcomments(),
            discardempty(),
            autoprefixer(config.autoprefixer)
        ]))
        .pipe($.sourcemaps.write('.'))
        .pipe(gulp.dest(config.publicDir + '/css'));
});

gulp.task('min', function () {
    return gulp.src([config.publicDir + '/css/*.css', '!' + config.publicDir + '/css/*.min.css'])
        .pipe($.cssmin(config.cssmin))
        .pipe($.rename({suffix: '.min'}))
        .pipe(gulp.dest(config.publicDir + '/css'))
        .pipe($.livereload());
});

gulp.task('scss_min', function (cb) {
    runSequence('scss', 'min', cb);
});


/*
 * Global
 */
gulp.task('watch', ['scss_min'], function () {
    $.livereload.listen();
    gulp.watch(
        [
            config.scssDir + '/*.scss',
            config.scssDir + '/**/*.scss'
        ],
        ['scss_min']);
});