package xiao.clone.detect.util;

public class Token {
	
	private String rawValue;
	private int number;
	
	public Token(String raw, int n){
		this.rawValue = raw;
		this.number = n;
	}

	public String getRawValue() {
		return rawValue;
	}

	public void setRawValue(String rawValue) {
		this.rawValue = rawValue;
	}

	public int getNumber() {
		return number;
	}

	public void setNumber(int number) {
		this.number = number;
	}

}
