#pragma once

#include "../core.h"

Object* clisp_make_int(int value);

int get_int_value(Object* obj);

void destroy_int(Object* obj);

Object* clisp_make_double(double value);

double get_double_value(Object* obj);

void destroy_double(Object* obj);

Object* clisp_make_boolean(unsigned char value);

Object* make_true();

Object* make_false();

unsigned char get_boolean_value(Object* obj);

void destroy_boolean(Object* obj);

Object* clisp_make_string(char* value);

char* get_string_value(Object* obj);

unsigned int get_string_length(Object* obj);

void destroy_string(Object* obj);

Object* clisp_make_char(char value);

char get_char_value(Object* obj);

void destroy_char(Object* obj);
