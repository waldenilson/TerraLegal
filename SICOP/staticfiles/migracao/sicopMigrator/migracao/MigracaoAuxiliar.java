package br.gov.incra.migracao;


import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;

public class MigracaoAuxiliar {

	private static String diretorio = "c:\\DEVELOPER/SICOP/Migracao/Report";
	private static String nomeArqMigracao = "scriptTbexemplo.sql";
	private static String nomeArqMunicipio = "municipio.sql";
	private static String nomeArqGleba = "gleba.sql";
	private static String nomeArqCaixa = "caixa.sql";
	private static String nomeArqSubarea = "subarea.sql";
	private static String nomeArqContrato = "contrato.sql";
	private static String nomeArqAuthUser = "auth_user.sql";
	private static String nomeArqSituacaogeo = "situacaogeo.sql";
	private static String nomeArqProcessoBase = "processobase.sql";
	private static String nomeArqTipoPendencia = "tipopendencia.sql";
	private static String nomeArqPregao = "pregao.sql";
	
	private static String nomeArqConjuge = "conjuge.txt";
	private static String nomeArqProcessosAnexos = "processosanexos.txt";
	
	private static String sisterlegPlanilha = "extrato_sisterleg_total_MA.txt";
	
	public static Map mapMunicipio() {	return ler(diretorio, nomeArqMunicipio,"\t",11,0, true); }
	public static Map mapGleba() {	return ler(diretorio, nomeArqGleba,"\t",3,1, true); }
	public static Map mapCaixa() {	return ler(diretorio, nomeArqCaixa,"\t",2,0, false); }
	public static Map mapSubarea() {	return ler(diretorio, nomeArqSubarea,"\t",3,1, false); }
	public static Map mapContrato() {	return ler(diretorio, nomeArqContrato,"\t",3,0, false); }
	public static Map mapAuthUser() {	return ler(diretorio, nomeArqAuthUser,"\t",11,3, false); }
	public static Map mapSituacaogeo() {	return ler(diretorio, nomeArqSituacaogeo,"\t",2,0, true); }
	public static Map mapProcessoBase() { return ler(diretorio, nomeArqProcessoBase,"\t",10,0, false); }
	public static Map mapTipoPendencia() { return ler(diretorio, nomeArqTipoPendencia,"\t",0,1, false); }
	public static Map mapPregao() { return ler(diretorio, nomeArqPregao,"\t",2,0, false); }
		
	public static Map mapNomeConjuge() { return ler(diretorio, nomeArqConjuge,"\t",2,0, false); }
	public static Map mapCPFConjuge() { return ler(diretorio, nomeArqConjuge,"\t",1,0, false); }

	public static Map mapProcessosAnexos() { return ler(diretorio, nomeArqProcessosAnexos,";", 1, 1, false); }
	
	public static Map mapSisterlegPlanilhaEndereco() { return ler(diretorio, sisterlegPlanilha,"\t", 16, 1, false); }
	public static Map mapSisterlegPlanilhaApelido() { return ler(diretorio, sisterlegPlanilha,"\t", 5, 1, false); }
	public static Map mapSisterlegPlanilhaConjuge() { return ler(diretorio, sisterlegPlanilha,"\t", 19, 1, false); }
	public static Map mapSisterlegPlanilhaTelefone() { return ler(diretorio, sisterlegPlanilha,"\t", 17, 1, false); }
	public static Map mapSisterlegPlanilhaMunicipio() { return ler(diretorio, sisterlegPlanilha,"\t", 26, 1, false); }
		
	public MigracaoAuxiliar()
	{		
		File dir = new File( diretorio );
		
//		System.out.println(mapMunicipio().size());
//		System.out.println(mapGleba().size());
//		System.out.println(mapCaixa().size());
//		System.out.println(mapSubarea().size());
//		System.out.println(mapContrato().size());
//		System.out.println(mapSituacaogeo().size());
			
//		escreve(todosScripts, new File(dir, nomeArqMigracao) );
	}
	
	public static void main(String a[])
	{
		new MigracaoAuxiliar();
	}
	
	
	public static Map ler(String diretorio, String nomeArq,String separador, int k, int v, boolean caixaalta)
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
		        	
		        	String[] s = cont.split(separador);
		        	
		        	if(caixaalta)
		        		mMunicipio.put( s[v].toUpperCase(),  s[k]);
		        	else
		        		mMunicipio.put( s[v], s[k] );
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
    
    public static String normalizarString(String txt)
	   {
			if(txt==null)
				return "";
			
			txt = Normalizer.normalize(txt,Normalizer.Form.NFD);
		    
			txt = txt.replaceAll("[^\\p{ASCII}]", "");
			return txt;
		}
		
}
