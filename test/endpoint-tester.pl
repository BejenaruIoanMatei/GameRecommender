#!/usr/bin/perl
use strict;
use warnings;
use LWP::UserAgent;
use JSON;
use URI::Escape;

sub test_endpoint {
    my ($method, $url, $data, $outfile) = @_;
    
    my $ua = LWP::UserAgent->new(timeout => 10);
    my $response;
    
    if ($method eq 'GET') {
        $response = $ua->get($url);
    } elsif ($method eq 'POST') {
        $response = $ua->post($url, 
            'Content-Type' => 'application/json',
            Content => encode_json($data)
        );
    }
    
    print "Status: " . $response->code . "\n";

    my $content = $response->decoded_content;

    print "Response:\n$content\n";

    eval {
        my $json_data = decode_json($content);
        my $pretty_json = to_json($json_data, { pretty => 1, utf8 => 1 });

        open(my $fh, '>:encoding(UTF-8)', $outfile) or die "Cant open the file '$outfile' write: $!";
        print $fh $pretty_json;
        close($fh);

        print "Saved response to $outfile\n";
    };
    if ($@) {
        warn "Failed decoding JSON: $@\n";
        open(my $fh, '>:encoding(UTF-8)', $outfile) or die "Cant open the file '$outfile' write: $!";
        print $fh $content;
        close($fh);

        print "Saved raw response to $outfile\n";
    }

    return $response->is_success;
}


my $title = 'battlefield 4';

my $escaped_title = uri_escape($title);

my $url_cosine = "http://127.0.0.1:8000/recommend/cosine?title=$escaped_title";
my $url_nn = "http://127.0.0.1:8000/recommend/nn?title=$escaped_title";
my $url_recommend = "http://127.0.0.1:8000/recommend/?title=$escaped_title";

test_endpoint('GET', $url_cosine, undef, 'test/response_cosine.json');
test_endpoint('GET', $url_nn, undef, 'test/response_nn.json');
test_endpoint('GET', $url_recommend, undef, 'test/response_recommend.json');