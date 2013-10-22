package br.gov.incra.migracao;


import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;

public class MigracaoAuxiliar {

	private String diretorio = "C:\\DEVELOPER/SICOP/Migracao/auxiliar";
	private String nomeArqMigracao = "scriptTbexemplo.sql";
	private String nomeArqMunicipio = "municipio.sql";
	private String nomeArqGleba = "gleba.sql";
	private String nomeArqCaixa = "caixa.sql";
	private String nomeArqSubarea = "subarea.sql";
	private String nomeArqContrato = "contrato.sql";
	private String nomeArqSituacaogeo = "situacaogeo.sql";
	
	
	
	public Map mapMunicipio() {	return ler(diretorio, nomeArqMunicipio,11,0); }
	public Map mapGleba() {	return ler(diretorio, nomeArqGleba,3,1); }
	public Map mapCaixa() {	return ler(diretorio, nomeArqCaixa,3,0); }
	public Map mapSubarea() {	return ler(diretorio, nomeArqSubarea,3,1); }
	public Map mapContrato() {	return ler(diretorio, nomeArqContrato,3,0); }
	public Map mapSituacaogeo() {	return ler(diretorio, nomeArqSituacaogeo,3,0); }
	
	public MigracaoAuxiliar()
	{		
		File dir = new File( diretorio );
		
		System.out.println(mapMunicipio().size());
		System.out.println(mapGleba().size());
		System.out.println(mapCaixa().size());
		System.out.println(mapSubarea().size());
		System.out.println(mapContrato().size());
		System.out.println(mapSituacaogeo().size());
			
//		escreve(todosScripts, new File(dir, nomeArqMigracao) );
	}
	
	public static void main(String a[])
	{
		new MigracaoAuxiliar();
	}
	
	
	public Map ler(String diretorio, String nomeArq, int k, int v)
	{
		
			File dir = new File( diretorio );
			File arq = new File(dir, nomeArq );
		 	
			
			try {
		        //Indicamos o arquivo que será lido
		        FileReader fileReader = new FileReader(arq);
		 
		        //Criamos o objeto bufferReader que nos
		        // oferece o método de leitura readLine()
		        BufferedReader bufferedReader =
		            new BufferedReader(fileReader);
		 
		        //String que irá receber cada linha do arquivo
		        String linha = "";
     	        
		        Map<String, String> mMunicipio = new HashMap<>();
	
		        while ( ( linha = bufferedReader.readLine() ) != null) 
		        {
		        	String cont = linha;
		        	String[] s = cont.split("\t");
		        	mMunicipio.put(s[k], s[v]);		        	
		        }
		        
		        fileReader.close();
		        bufferedReader.close();
		        return mMunicipio;
		    } catch (IOException e) {
		        e.printStackTrace();
		        return null;
		    }

	}
	
	// método para escrever no TXT  
    public void escreve (String conteudo, File arq){  
          
        try {  
            FileWriter escreve = new FileWriter(arq, true);  
            conteudo += System.getProperty("line.separator"); // pular linha  
            escreve.write(conteudo); // escrever o conteúdo  
            escreve.close();  
        } catch (IOException e) {  
            // TODO Auto-generated catch block  
            e.printStackTrace();  
        }  
    }  
		
}
