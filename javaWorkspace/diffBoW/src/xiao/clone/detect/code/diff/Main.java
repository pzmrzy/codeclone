package xiao.clone.detect.code.diff;

import org.json.simple.JSONObject;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;

import org.eclipse.jdt.core.compiler.InvalidInputException;
import org.json.simple.JSONArray;
import org.json.simple.parser.ParseException;

import xiao.clone.detect.util.Token;
import xiao.clone.detect.util.Tokenizer;

import org.json.simple.parser.JSONParser;

public class Main {

	public static void main(String[] args) throws IOException, ParseException, InvalidInputException {
		JSONParser parser = new JSONParser();
		String javaPath = "D:/codeclone/preprocess/antlr3_java.json";
		String csPath = "D:/codeclone/preprocess/antlr3_csharp.json";
		Object obj = parser.parse(new FileReader(csPath));
		JSONObject diff = (JSONObject) obj;
		for (Object o : diff.entrySet()) {
			Entry entry = (Entry) o;
			JSONObject jsonObject = (JSONObject) entry.getValue();
			JSONArray code = (JSONArray) jsonObject.get("code");
			Iterator<String> iterator = code.iterator();
			String str = "";
			boolean comment = false;
			while (iterator.hasNext()) {
				String line = iterator.next();
				if ((line.startsWith("+") && !line.startsWith("++"))
						|| (line.startsWith("-") && !line.startsWith("--"))) {
					line = line.substring(1);
				}
				while (line.startsWith("\t") || line.startsWith(" ")) {
					line = line.substring(1);
				}
				


				if (line.startsWith("#set"))
					continue;

				if (line.startsWith("*"))
					continue;

				int count = 0;
				for (int i = 0; i < line.length(); i++) {
					char c = line.charAt(i);
					if (c == '\'') {
						count++;
					}
				}
				if (count % 2 != 0) {
					continue;
				}
				
				if (line.equals("\ufeff/*"))
					continue;

				if (line.startsWith("/*")) {
					comment = true;
					continue;
				}
				if (line.startsWith("*/")) {
					comment = false;
					continue;
				}
				if (comment == false) {
					line = line.replaceAll("[^a-zA-Z]", " ");
					str += line + '\n';
				}
			}
			Tokenizer tokenizer = new Tokenizer();
			System.out.println(str);
			List<Token> tokenList = tokenizer.tokenize(str);
			String src = "";
			for (Token token : tokenList) {
				src += token.getRawValue() + " ";
			}
			if (!src.equals("")) {
				// System.out.println(src);
				jsonObject.put("token_stream", src);
			}
		}
		// System.out.println(diff.toJSONString());
		FileWriter file = new FileWriter("D:/codeclone/preprocess/antlr3_csharp_new.json");
		file.write(diff.toJSONString());
	}
}
