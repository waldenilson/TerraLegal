package br.gov.incra.migracao;


import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class MigracaoSituacaoProcesso {

	private String diretorio = "C:\\DEVELOPER/SICOP/Migracao";
	private String nomeArqMigracao = "scriptTbsituacaoprocesso.sql";
	private String nomeArqLegado = "dump_tbprocessourbano.txt";
	
	public MigracaoSituacaoProcesso()
	{		
		File dir = new File( diretorio );
		String todosScripts = "";
			String conteudo = ler(diretorio, nomeArqLegado);
			todosScripts += conteudo;
		escreve(todosScripts, new File(dir, nomeArqMigracao) );
	}
	
	public static void main(String a[])
	{
		new MigracaoSituacaoProcesso();
	}
	
	
	public String ler(String diretorio, String nomeArq)
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
		        String conteudo = "";
		        String tabela = nomeArq.substring(5, nomeArq.length()-4);
	//	        System.out.println("table: "+tabela);
		        
		        
		        
		        //Fazemos um loop linha a linha no arquivo,
		        // enquanto ele seja diferente de null.
		        //O método readLine() devolve a linha na
		        // posicao do loop para a variavel linha.
		        int x = 1;
		        List<String> l1 = new ArrayList<String>();
	        	List<String> l2 = new ArrayList<String>();
	        	while ( ( linha = bufferedReader.readLine() ) != null) {
		            
		        	//Aqui imprimimos a linha
	//	        	tabela = "tbconjuge";
		        	
	//	        	String cont = linha.replaceAll("\t", ",");
		        	String cont = linha;
		        	String contaux = "";
		        	String[] s = cont.split(";");
		        		        	
		        	
		        	for(int y=0; y < s.length ; y++)
		        	{
		        		String aux = "";
		        		String a = s[y];
		        		
		        		a = a.replaceAll("\"", "");
		        		a = a.trim();
		        		
		        		if (a.startsWith("20") && a.contains("-") && a.contains(":"))
		        			aux = "'"+a+"'";
	
		        		else if (a.startsWith("{") && a.endsWith("}") )
		        			aux = "'"+a+"'";
		        		
		        		else
		        		
		        			aux = "'"+a+"'";
		        		

		        		if(y==15)
		    		        l1.add(aux);
		        					        		
		        		contaux += aux+"\t";
		        		
		        	}
		        	
		        	cont = contaux.substring(0,contaux.length()-1);		        	
	        		cont = cont.replaceAll("\t", ",");
	        		cont = cont.replaceAll(",,", ",null,");
	        		cont = cont.replaceAll(",,", ",null,");
	        		cont = cont.replaceAll("''", "null");
		        	x++;
		        }

//	        	MONTANDO A LISTA COM TODOS OS REGISTROS
	        	ArrayList<String> lbd = new ArrayList<String>();
	        	System.out.println("total: "+l1);
	        	for(String a : l1)
	        	{
	        		String cont = a+",'',1";
			        tabela = "tbsituacaoprocesso";
		        	lbd.add("INSERT INTO "+tabela+" values( "+cont+" );");
	        	}
	        	
//	        	APLICANDO O DISTINCT NOS REGISTROS
	        	ArrayList<String> lbd2 = new ArrayList<String>();
	        	for(String a : lbd)
	        	{
	        		boolean achou = false;
	        		for(String b : lbd2)
	        		{
		        		if( b.equals(a) )
		        			achou = true;
	        		}
	        		if(!achou)
	        			lbd2.add(a);			    
	        	}
	        	
	        	
//	        	MONTANDO STRING DO CONTEUDO
	        	String content="";
	        	for(String a : lbd2)
	        		content += a+"\n";
	        	conteudo = content;

	        	fileReader.close();
		        bufferedReader.close();
		        return conteudo;
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
