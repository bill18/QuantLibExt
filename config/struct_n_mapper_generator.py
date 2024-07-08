import re
import io
import json

# https://stackoverflow.com/questions/7152762/how-to-redirect-print-output-to-a-file

# the following makes code simple, but it may hide some of the values which need to be converted
def map_value(val):
    value_map = {
        ""                        : ""                                   ,
        "0"                       : "0"                                  ,
        "0.0"                     : "0.0"                                ,
        "{}"                      : "{}"                                 ,
        "true"                    : "true"                               ,
        "false"                   : "false"                              ,
        "std::vector<bool>(0)"    : "std::vector<bool>(0)"               ,
        "Pillar::LastRelevantDate": "QuantLib::Pillar::LastRelevantDate" ,
        "Null<Natural>()"         : "QuantLib::Null<QuantLib::Natural>()",
        "Date()"                  : "QuantLib::Date()"                   ,
        "0 * Days"                : "0 * QuantLib::Days"                 ,
        "ext::nullopt"            : "QuantLib::ext::nullopt"             ,
        "RateAveraging::Compound" : "QuantLib::RateAveraging::Compound"  ,
        "Following"               : "QuantLib::Following"                ,
        "Annual"                  : "QuantLib::Annual"                   ,
        "Unadjusted"              : "QuantLib::Unadjusted"               ,
        "Calendar()"              : "QuantLib::Calendar()"               ,
        "NullCalendar()"          : "QuantLib::NullCalendar()"           ,
        "Futures::IMM"            : "QuantLib::Futures::IMM"             ,
    }

    # TODO: remove existance checking to make it expose problems
    return value_map[val] # if val in value_map else val

def map_func(tname, vname):
    func_map = {
        "Handle<YieldTermStructure>"          : "context.getYieldTermStructure",
        "ext::shared_ptr<BMAIndex>"           : "context.getBmaIndex"                                     ,
        "ext::shared_ptr<IborIndex>"          : "context.getIborIndex"                                    ,
        "ext::shared_ptr<OvernightIndex>"     : "context.getOvernightIndex"                               ,
        "ext::shared_ptr<SwapIndex>"          : "context.getSwapIndex"                                    ,
    }
    vname = 'v.%s' % vname
    pattern = 'Handle<(.*)>'
    matched = re.search(pattern, tname, flags=re.S)
    if matched:
        tname2 = matched.group(1)
        if not tname2.startswith('QuantLib::'):
            tname2 = 'QuantLib::' + tname2
        if tname2 == 'QuantLib::Quote':
            return 'QuantLib::Handle<%s>(%s(%s))' % (tname2, func_map[tname], vname) if tname in func_map else 'QuantLib::Handle<%s>(QuantLib::ext::make_shared<QuantLib::SimpleQuote>(%s))' % (tname2, vname)
        else:
            return 'QuantLib::Handle<%s>(%s(%s))' % (tname2, func_map[tname], vname) if tname in func_map else 'QuantLib::Handle<%s>(%s)' % (tname2, vname)
    else:
        return '%s(%s)' % (func_map[tname], vname) if tname in func_map else vname

        # auto quote = ext::make_shared<SimpleQuote>(value);


def map_type(tname):
    type_map = {
        "bool"                                : "bool"                                                    ,
        "BusinessDayConvention"               : "QuantLib::BusinessDayConvention"                         ,
        "Calendar"                            : "QuantLib::Calendar"                                      ,
        "Date"                                : "QuantLib::Date"                                          ,
        "DateGeneration::Rule"                : "QuantLib::DateGeneration::Rule"                          ,
        "DayCounter"                          : "QuantLib::DayCounter"                                    ,
        "double"                              : "double"                                                  ,
        "ext::optional<bool>"                 : "QuantLib::ext::optional<bool>"                           ,
        "ext::optional<BusinessDayConvention>": "QuantLib::ext::optional<QuantLib::BusinessDayConvention>",
        "ext::optional<DateGeneration::Rule>" : "QuantLib::ext::optional<QuantLib::DateGeneration::Rule>" ,
        "ext::optional<Frequency>"            : "QuantLib::ext::optional<QuantLib::Frequency>"            ,
        "ext::optional<Period>"               : "QuantLib::ext::optional<QuantLib::Period>"               ,
        "ext::shared_ptr<BMAIndex>"           : "std::string"                                             ,
        "ext::shared_ptr<IborIndex>"          : "std::string"                                             ,
        "ext::shared_ptr<OvernightIndex>"     : "std::string"                                             ,
        "ext::shared_ptr<SwapIndex>"          : "std::string"                                             ,
        "Frequency"                           : "QuantLib::Frequency"                                     ,
        "Futures::Type"                       : "QuantLib::Futures::Type"                                 ,
        "Handle<Quote>"                       : "QuantLib::SimpleQuote"                                   ,
        "Handle<YieldTermStructure>"          : "std::string"                                             ,
        "int"                                 : "int"                                                     ,
        "Integer"                             : "QuantLib::Integer"                                       ,
        "Natural"                             : "QuantLib::Natural"                                       ,
        "Period"                              : "QuantLib::Period"                                        ,
        "Pillar::Choice"                      : "QuantLib::Pillar::Choice"                                ,
        "Rate"                                : "QuantLib::Rate"                                          ,
        "RateAveraging::Type"                 : "QuantLib::RateAveraging::Type"                           ,
        "Real"                                : "QuantLib::Real"                                          ,
        "Schedule"                            : "QlExt::Schedule"                                         ,
        "Spread"                              : "QuantLib::Spread"                                        ,
        "std::vector<bool>"                   : "std::vector<bool>"                                       ,
        "std::vector<Date>"                   : "std::vector<QuantLib::Date>"                             ,
        "Swap::Type"                          : "QuantLib::Swap::Type"                                    ,
    }

    # not to check the existance, so that the problems can be exposed
    return type_map[tname]

def get_args(content, ctype, ver):
    tmp = content.split(',')
    tmp = [t.strip() for t in tmp]
    tmp = [t.replace('&', '') for t in tmp]
    tmp = [t.replace('const ', '') for t in tmp]
    tmp = [t.split('=', 1) for t in tmp]
    # print('......... tmp 1 .........')
    # print(tmp)
    dvals = [t[1].strip() if len(t) > 1 else '' for t in tmp]
    # print('......... dvals 1 .........')
    # print(dvals)    
    decls = [t[0].strip().rsplit(' ', 1) for t in tmp]
    # print('......... decls 1 .........')
    # print(decls)

    decls = [(a[0], a[1], b) for a, b in zip(decls, dvals)]
    tmp = [(map_type(t), n, map_value(d), t) for (t, n, d) in decls]
    common = [
        ('std::string', '_type_', '"%s%s"' % (ctype, ver), 'std::string'),
        # ('std::string', '_ver_' , '', 'std::string'),
    ]

    if len(ver) > 0:
        common.append(('std::string', '_ver_' , '"%s"' % ver, 'std::string'))

    return common + tmp

        
def get_ctors(ctors):
    # remove comments
    ctors = re.sub(r'//.*?\n|/\*.*?\*/', '', ctors, flags=re.S)
    # print(ctors)
    ctor_idx = {}
    ctor_pattern = r'(\w+::)?(\w+)\s*\((.*)\)'
    ctor_list = ctors.split(';')
    # pre-build (name, content) pairs to make sure how may cases do we have
    # this way, we will have whether to add "_ver_" or not

    context_idx = {}
    for ctor in ctor_list:
        ctor = ctor.strip()
        if len(ctor) == 0:
            continue

        matched = re.search(ctor_pattern, ctor, flags=re.S)
        if matched:
            name = matched.group(2).strip()
            content = matched.group(3).strip()
            # print('............... content ..................')
            # print(content)
            # if not name in context_idx:
            #     context_idx[name] = []
            # context_idx[name].append(content)
            context_idx.setdefault(name, []).append(content)

    # if name == 'BMASwapRateHelper':
    #     print('---- debug ----')
    #     print(ctors)
    #     print('---------------')
    #     print(json.dumps(context_idx, indent=2))

    for name, signatures in context_idx.items():
        multipe_ver = len(signatures)>1
        for i, signature in enumerate(signatures):
            ver = 'V%s' % i if multipe_ver else ''
            # if not name in ctor_idx:
            #     ctor_idx[name] = []
            # ctor_idx[name].append(get_args(signature, ver))
            ctor_idx.setdefault(name, []).append(get_args(signature, name, ver))


    # for ctor in ctor_list:
    #     ctor = ctor.strip()
    #     matched = re.search(ctor_pattern, ctor, flags=re.S)
    #     if matched:
    #         name = matched.group(2).strip()
    #         content = matched.group(3).strip()
    #         # print('............... content ..................')
    #         # print(content)
    #         if not name in ctor_idx:
    #             ctor_idx[name] = []
    #         ctor_idx[name].append(get_args(content))
    
    return ctor_idx

def gen_single_struct(output, struct_name, decls, ver='', indent=''):
    print('%sstruct %s {' % (indent, struct_name), file=output)
   #  print(indent+'   std::string _name_;', file=output)
   #  print(indent+'   std::string _ver_;' , file=output)
    # if len(ver) > 0:
    #     print(indent+'   %-35s %-20s = %-35s;' % ('std::string', '_ver_', '"%s"' % ver), file=output)
    for tvp in decls:
        if len(tvp[2]) == 0:
            print(indent+'   %-35s %-58s;' % (tvp[0], tvp[1]), file=output)
        else:
            print(indent+'   %-35s %-20s = %-35s;' % tvp[:3], file=output)
    print('%s};\n' % indent, file=output)


def gen_main_struct(output, struct_name, val, indent=''):
    vtypes = []
    for i, v in enumerate(val):
        vtypes.append('%sV%s' % (struct_name, i))

    print('%susing %s = std::variant<%s>;' % (indent, struct_name, ','.join(vtypes)), file=output);

    
def gen_structs(output, name_space, ctor_idx, struct_name, indent='   '):
    print('namespace %s {' % name_space, file=output)
    for key, val in ctor_idx.items():
        struct_name = struct_name
        if len(val) == 0:
            continue
        if len(val) == 1:
            gen_single_struct(output, struct_name, val[0], '', '      ')
        else:
            # print('   namespace %s {' % struct_name, file=output)
            for i, v in enumerate(val):
                gen_single_struct(output, '%sV%s' % (struct_name, i), v, 'V%s' %i, '      ')

            gen_main_struct(output, struct_name, val, indent='      ')
            # print('   }', file=output)
    print('}', file=output)
    print('', file=output)

def gen_obj_creator(output, clazz, key, val, indent='   '):
    print('inline QuantLib::ext::shared_ptr<QuantLib::%s> create(const QlExt::Context& context, const %s& v) {' % (key, clazz), file=output)
    print('%sreturn QuantLib::ext::make_shared<QuantLib::%s> (' % (indent, key), file=output)
    i = 0
    for tvp in val:
        if tvp[1] == '_name_' or tvp[1] == '_ver_':
            continue

        if i>0:
            print(',', file=output)
        print(indent+'   %s' % map_func(tvp[3], tvp[1]), end='', file=output)
        i += 1

    print('', file=output)
    print('%s);' % indent, file=output)
    print('}', file=output)
    print('', file=output)

def gen_obj_creators(output, ctor_idx, struct_name, name_space, indent='   '):
    for key, val in ctor_idx.items():
        if len(val) == 0:
            continue
        struct_name = struct_name
        if len(val) == 1:
            gen_obj_creator(output, '%s::%s' % (name_space, struct_name), key, val[0])
        else:
            for i, v in enumerate(val):
                gen_obj_creator(output, '%s::%sV%s' % (name_space, struct_name, i), key, v, '   ')

# ----------------------------------------------------------------------------------------------
def gen_to_from_json_header_tmpl(namespace, defs, struct_name, func):
    for key, val in defs.items():
        if len(val) == 0:
            continue
        clazz = struct_name if len(namespace) == 0 else (namespace + '::' + struct_name)
        func(clazz)

        if len(val) > 1:
            for i, v in enumerate(val):
                clazz = struct_name + 'V' + str(i) if len(namespace) == 0 else (namespace + '::' + struct_name + 'V' + str(i))
                func(clazz)

def gen_from_json_header(output, namespace, defs, struct_name):
    gen_to_from_json_header_tmpl(namespace, defs, struct_name, lambda clazz: print('void from_json(%s& v, const nlohmann::json& j);' % clazz, file=output))

def gen_from_json_vector_header(output, namespace, defs, struct_name):
    gen_to_from_json_header_tmpl(namespace, defs, struct_name, lambda clazz: print('void from_json(std::vector<%s>& v, const nlohmann::json& j);' % clazz, file=output))

def gen_to_json_header(output, namespace, defs, struct_name):
    gen_to_from_json_header_tmpl(namespace, defs, struct_name, lambda clazz: print('nlohmann::json to_json(const %s& v);' % clazz, file=output))

def gen_to_json_vector_header(output, namespace, defs, struct_name):
    gen_to_from_json_header_tmpl(namespace, defs, struct_name, lambda clazz: print('nlohmann::json to_json(const std::vector<%s>& v);' % clazz, file=output))

# ----------------------------------------------------------------------------------------------
def gen_to_from_json_body_tmpl(namespace, defs, struct_name, func, func2=None):
    for key, val in defs.items():
        if len(val) == 0:
            continue
        if len(val) == 1:
            clazz = struct_name if len(namespace) == 0 else (namespace + '::' + struct_name)
            func(clazz, val[0])
        else:
            if func2 is not None:
                clazz = struct_name if len(namespace) == 0 else (namespace + '::' + struct_name)
                func2(clazz, val)

            for i, v in enumerate(val):
                clazz = struct_name + 'V' + str(i) if len(namespace) == 0 else (namespace + '::' + struct_name + 'V' + str(i))
                func(clazz, v)

def gen_main_from_json_body(output, clazz, decls):
    print('void from_json(%s& v, const nlohmann::json& j) {' % clazz, file=output)
    first = True
    for i, decl in enumerate(decls):
        # ver = decl['_ver_']
        ver = 'V%s' % i
        print('   if j["_ver_"] == "%s" {' % ver, file=output)
        print('      %sV%s obj;' % (clazz, i), file=output)
        print('      from_json(obj, j);', file=output)
        print('      return;', file=output)
        print('   }', file=output)
        print('', file=output)
    print("}\n", file=output)

def gen_single_from_json_body(output, clazz, decls):
    print('void from_json(%s& v, const nlohmann::json& j) {' % clazz, file=output)
    print('   for (const auto& [key, val] : j.items()) {', file=output)
    first = True
    for df in decls:
        vname = df[1]
        els = 'else ' if not first else ''
        print('      %sif (key == "%s")' % (els, vname), file=output)
        print('         from_json(v.%s, val);' % vname, file=output)
    print("   }\n", file=output)
    print("}\n", file=output)

def gen_from_json_body(output, namespace, defs, struct_name):
    gen_to_from_json_body_tmpl(namespace, defs, struct_name, 
                               lambda clazz, defs: gen_single_from_json_body(output, clazz, defs),
                               lambda clazz, defs: gen_main_from_json_body(output, clazz, defs))

def gen_single_from_json_vector_body(output, clazz, decls):
    vname = 't'
    print('void from_json(std::vector<%s>& v, const nlohmann::json& j) {' % clazz, file=output)
    print('     for (const auto& val : j) {', file=output)
    print('           %s %s;' % (clazz, vname), file=output)
    print('           from_json(%s, val);' % vname, file=output)
    print('           v.push_back(%s);' % vname, file=output)
    print("     }\n", file=output)
    print(" }\n", file=output)

def gen_from_json_vector_body(output, namespace, defs, struct_name):
    gen_to_from_json_body_tmpl(namespace, defs, struct_name, lambda clazz, defs: gen_single_from_json_vector_body(output, clazz, defs))


def gen_main_to_json_body(output, clazz, decls):
    print('nlohmann::json to_json(const %s& v) {' % clazz, file=output)
    for i, decl in enumerate(decls):
        ver = '%sV%s' % (clazz, i)
        print('   if (std::holds_alternative<%s>(v)) {' % ver, file=output)
        print('      if (auto p = std::get_if<%s>(&v)) {' % ver, file=output)
        print('         return to_json(*p);', file=output)
        print('      }', file=output)
        print('   }', file=output)
        print('', file=output)
    print('   return nlohmann::json{};', file=output)
    print("}\n", file=output)


def gen_single_to_json_body(output, clazz, defs):
    print('nlohmann::json to_json(const %s& v) {' % clazz, file=output)
    print('   nlohmann::json j = {', file=output)
    # first = True
    for df in defs:
        vname = df[1]
        left = '"%s"' % vname
        right= 'to_json(v.%s)' % vname
        print('      {%-23s,  %-32s},' % (left, right), file=output)
    print("   };", file=output)
    print("", file=output)
    print("   return j;", file=output)
    print("}\n", file=output)

def gen_to_json_body(output, namespace, defs, struct_name):
    gen_to_from_json_body_tmpl(namespace, defs, struct_name, 
                               lambda clazz, defs: gen_single_to_json_body(output, clazz, defs),
                               lambda clazz, defs: gen_main_to_json_body(output, clazz, defs))

def gen_single_to_json_vector_body(output, clazz, defs):
    print('nlohmann::json to_json(const std::vector<%s>& v) {' % clazz, file=output)
    print('   nlohmann::json j = {};', file=output)
    print('   for (const auto& t: v) {', file=output)
    print('      j.push_back(to_json(t));', file=output)
    print('   }', file=output)
    print("   return j;", file=output)
    print("}\n", file=output)


def gen_to_json_vector_body(output, namespace, defs, struct_name):
    gen_to_from_json_body_tmpl(namespace, defs, struct_name, lambda clazz, defs: gen_single_to_json_vector_body(output, clazz, defs))


def gen_includes(output):
    INCS = """#include <iostream>
#include <iomanip>
#include <unordered_map>
#include <vector>
#include <variant>
#include <ql/quantlib.hpp>
#include <ql/optional.hpp>
#include <ql/handle.hpp>
#include "JsonUtils.h"
#include "Structs.h"
"""
    print(INCS, file=output)


def prepand_extra_fields(ctor_idx, cfg):
    if 'extra_fields' in cfg:
        extra_fields = cfg['extra_fields']
        for name in ctor_idx:
            for ctor in ctor_idx[name]:
                for field in extra_fields:
                    ctor.insert(0, (field['type'], field['name'], field['value'], field['type']))
    # print(json.dumps(ctor_idx, indent=2))


def gen_code(cfg_file):
    with open(cfg_file, 'r') as f:
        config = json.load(f)
        for cfg in config:
            struct_name = cfg['struct_name']
            name_space = cfg['name_space']
            file_name = cfg['tgt_file_name']

            with open('config/%s' % cfg['ctor_file'], 'r') as ctor_file:
                ctor_idx = get_ctors(ctor_file.read())
                prepand_extra_fields(ctor_idx, cfg)
                # print(json.dumps(ctor_idx, indent=2))

                with open('../../helpers/src/%s.h' % file_name, 'w') as header:
                    gen_includes(header)
                    gen_structs(header, name_space, ctor_idx, struct_name)
                    gen_obj_creators(header, ctor_idx, struct_name, name_space)
                    gen_from_json_header(header, name_space, ctor_idx, struct_name)
                    gen_from_json_vector_header(header, name_space, ctor_idx, struct_name)
                    gen_to_json_header(header, name_space, ctor_idx, struct_name)      
                    gen_to_json_vector_header(header, name_space, ctor_idx, struct_name)
                    header.close()

                with open('../../helpers/src/%s.cpp' % file_name, 'w') as body:
                    print('#include "%s.h"' % file_name, file=body)
                    print('', file=body)
                    gen_from_json_body(body, name_space, ctor_idx, struct_name)
                    gen_from_json_vector_body(body, name_space, ctor_idx, struct_name)
                    gen_to_json_body(body, name_space, ctor_idx, struct_name)
                    gen_to_json_vector_body(body, name_space, ctor_idx, struct_name)
                    body.close()

def test_optional_extractor():
    s = "QuantLib::ext::optional<QuantLib::BusinessDayConvention>"
    opt_pattern = r'QuantLib::ext::optional<(.*)>'
    matched = re.search(opt_pattern, s, flags=re.S)
    if matched:
        print(matched.group(1))

if __name__ == '__main__':
    cfg_file = 'config/code_gen.cfg'
    gen_code(cfg_file)
    # test_optional_extractor()
