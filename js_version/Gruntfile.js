'use strict';

module.exports = function(grunt) {

    // Project Configuration
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        compass: {
            dist: {
              options: {
                   config: 'config.rb'
               }
            }
        },
        watch: {
           options: {
                livereload: false
            },
            scripts: {
                files: ['index.html', '/scss/**/*', '/js/**/*.js'],
                tasks: ['default'],
                options: {
                    nospawn: true
                }
            }
       },
       connect: {
           server: {
                options: {
                    port: 9000,
                    hostname: 'localhost',
                    keepalive: true
                }
           }
       }
    });

    // Load plugins
    grunt.loadNpmTasks('grunt-contrib-compass');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-connect');

    // Register Tasks
    grunt.registerTask('default', ['compass', 'watch']);
    grunt.registerTask('server', ['connect']);
    grunt.registerTask('build', ['compass']);
};
