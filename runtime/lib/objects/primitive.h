#pragma once

#include "lib/core.h"

CL_Object* cl_make_int(int value);

int cl_get_int_value(CL_Object* obj);

void cl_destroy_int(CL_Object* obj);

CL_Object* cl_make_double(double value);

double cl_get_double_value(CL_Object* obj);

void cl_destroy_double(CL_Object* obj);

CL_Object* cl_make_boolean(unsigned char value);

CL_Object* cl_make_true();

CL_Object* cl_make_false();

unsigned char cl_get_boolean_value(CL_Object* obj);

void cl_destroy_boolean(CL_Object* obj);

CL_Object* cl_make_string(char* value);

char* cl_get_string_value(CL_Object* obj);

unsigned int cl_get_string_length(CL_Object* obj);

void cl_destroy_string(CL_Object* obj);

CL_Object* cl_make_char(char value);

char cl_get_char_value(CL_Object* obj);

void cl_destroy_char(CL_Object* obj);

CL_Object* cl_to_integer(CL_FUNC_PARAMS);

CL_Object* cl_to_double(CL_FUNC_PARAMS);

CL_Object* cl_to_char(CL_FUNC_PARAMS);

CL_Object* cl_to_string(CL_FUNC_PARAMS);

CL_Object* cl_to_boolean(CL_FUNC_PARAMS);
